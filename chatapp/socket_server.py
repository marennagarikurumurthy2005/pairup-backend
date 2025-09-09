import socketio
from datetime import datetime, timezone, timedelta
import threading
import time
from chatapp.models import ChatMessage, ReadStatus
from users.models import User

sio = socketio.Server(cors_allowed_origins='*')

# Track connected users
connected_users = {}

# Queue of messages to auto-delete
auto_delete_queue = []

# Lock for thread-safe operations on the queue
queue_lock = threading.Lock()

# -------------------- SOCKET EVENTS -------------------- #
@sio.event
def connect(sid, environ):
    print("Client connected:", sid)

@sio.event
def disconnect(sid):
    print("Client disconnected:", sid)
    connected_users.pop(sid, None)

@sio.event
def register(sid, data):
    user_id = data.get("user_id")
    try:
        user = User.objects.get(id=user_id)
        connected_users[sid] = user
        print(f"User {user.username} connected via socket")
    except User.DoesNotExist:
        pass

@sio.event
def send_message(sid, data):
    sender = connected_users.get(sid)
    receiver_id = data.get("receiver_id")
    message_text = data.get("message")
    if not sender or not receiver_id or not message_text:
        return

    try:
        receiver = User.objects.get(id=receiver_id)
        msg = ChatMessage.objects.create(sender=sender, receiver=receiver, message=message_text)
        ReadStatus.objects.create(message=msg)

        payload = {
            "id": msg.id,
            "sender": sender.username,
            "receiver": receiver.username,
            "message": message_text,
            "timestamp": str(msg.timestamp),
            "read": False,
            "read_at": None
        }

        # Emit to receiver if online
        for rsid, ruser in connected_users.items():
            if ruser.id == receiver.id:
                sio.emit("receive_message", payload, to=rsid)

        # Emit to sender
        sio.emit("message_sent", payload, to=sid)

        # Add to auto-delete queue
        delete_time = msg.timestamp + timedelta(hours=msg.expiry_hours)
        with queue_lock:
            auto_delete_queue.append((msg.id, delete_time))

    except User.DoesNotExist:
        pass

@sio.event
def mark_read(sid, data):
    user = connected_users.get(sid)
    message_id = data.get("message_id")
    if not user or not message_id:
        return

    try:
        msg = ChatMessage.objects.get(id=message_id, receiver=user)
        if msg.is_deleted:
            return

        read_status = getattr(msg, "read_status", None)
        if read_status and not read_status.read:
            read_status.read = True
            read_status.read_at = datetime.now(timezone.utc)
            read_status.save()

            # Notify sender if online
            for rsid, ruser in connected_users.items():
                if ruser.id == msg.sender.id:
                    sio.emit("message_read", {
                        "message_id": msg.id,
                        "read_at": str(read_status.read_at)
                    }, to=rsid)

    except ChatMessage.DoesNotExist:
        pass

@sio.event
def typing(sid, data):
    sender = connected_users.get(sid)
    receiver_id = data.get("receiver_id")
    if not sender or not receiver_id:
        return
    for rsid, ruser in connected_users.items():
        if ruser.id == receiver_id:
            sio.emit("typing", {"sender": sender.username}, to=rsid)

# -------------------- AUTO DELETE SCHEDULER -------------------- #
def auto_delete_scheduler():
    while True:
        now = datetime.now(timezone.utc)
        with queue_lock:
            for msg_tuple in auto_delete_queue[:]:
                msg_id, delete_time = msg_tuple
                if now >= delete_time:
                    try:
                        msg = ChatMessage.objects.get(id=msg_id)
                        if not msg.is_deleted:
                            msg.deleted_at = now
                            msg.save()

                            payload = {"message_id": msg.id, "deleted_at": str(now)}
                            # Notify both sender and receiver if online
                            for sid, user in connected_users.items():
                                if user.id in (msg.sender.id, msg.receiver.id):
                                    sio.emit("message_deleted", payload, to=sid)
                    except ChatMessage.DoesNotExist:
                        pass
                    auto_delete_queue.remove(msg_tuple)
        time.sleep(10)  # check every 10 seconds

# Start scheduler thread
threading.Thread(target=auto_delete_scheduler, daemon=True).start()

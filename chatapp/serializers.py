from rest_framework import serializers
from .models import ConnectionRequest, ChatMessage, ReadStatus, CallRequest
from users.serializers import PublicUserSerializer

class ConnectionRequestSerializer(serializers.ModelSerializer):
    from_user = PublicUserSerializer(read_only=True)
    to_user = PublicUserSerializer(read_only=True)

    class Meta:
        model = ConnectionRequest
        fields = "__all__"

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = PublicUserSerializer(read_only=True)
    receiver = PublicUserSerializer(read_only=True)
    read_status = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = "__all__"

    def get_read_status(self, obj):
        if hasattr(obj, "read_status"):
            return {"read": obj.read_status.read, "read_at": obj.read_status.read_at}
        return {"read": False, "read_at": None}

class CallRequestSerializer(serializers.ModelSerializer):
    from_user = PublicUserSerializer(read_only=True)
    to_user = PublicUserSerializer(read_only=True)

    class Meta:
        model = CallRequest
        fields = "__all__"

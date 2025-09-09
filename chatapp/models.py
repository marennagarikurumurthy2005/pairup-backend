from django.db import models
from user.models import User

class ConnectionRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")
        ordering = ["-timestamp"]

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="chat_images/", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    edited = models.BooleanField(default=False)
    expiry_hours = models.IntegerField(default=24)  # message auto-delete after n hours

    @property
    def is_deleted(self):
        from django.utils import timezone
        if self.deleted_at:
            return True
        if self.timestamp + timezone.timedelta(hours=self.expiry_hours) < timezone.now():
            return True
        return False

class ReadStatus(models.Model):
    message = models.OneToOneField(ChatMessage, on_delete=models.CASCADE, related_name="read_status")
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

class CallRequest(models.Model):
    CALL_TYPE = [
        ("audio", "Audio"),
        ("video", "Video"),
    ]
    from_user = models.ForeignKey(User, related_name="sent_calls", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_calls", on_delete=models.CASCADE)
    call_type = models.CharField(max_length=5, choices=CALL_TYPE)
    accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

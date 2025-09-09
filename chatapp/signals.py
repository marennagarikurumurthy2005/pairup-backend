from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ChatMessage, ReadStatus
from chatapp.socket_server import sio  # import your socketio server instance

@receiver(post_save, sender=ChatMessage)
def create_read_status(sender, instance, created, **kwargs):
    if created:
        ReadStatus.objects.create(message=instance)

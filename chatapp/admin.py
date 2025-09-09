from django.contrib import admin
from .models import ConnectionRequest, ChatMessage, ReadStatus, CallRequest

admin.site.register(ConnectionRequest)
admin.site.register(ChatMessage)
admin.site.register(ReadStatus)
admin.site.register(CallRequest)

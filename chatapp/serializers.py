# chatapp/serializers.py
from rest_framework import serializers
from .models import ConnectionRequest, ChatMessage, ReadStatus, CallRequest
from user.models import User


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "mobile"]


class ConnectionRequestSerializer(serializers.ModelSerializer):
    from_user = PublicUserSerializer(read_only=True)
    to_user = PublicUserSerializer(read_only=True)

    class Meta:
        model = ConnectionRequest
        fields = "__all__"


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = PublicUserSerializer(read_only=True)
    receiver = PublicUserSerializer(read_only=True)   # ✅ only output
    receiver_id = serializers.IntegerField(write_only=True)  # ✅ only input

    class Meta:
        model = ChatMessage
        fields = ["id", "sender", "receiver", "receiver_id",
                  "message", "image", "timestamp", "edited"]

    def create(self, validated_data):
        receiver_id = validated_data.pop("receiver_id")
        receiver = User.objects.get(id=receiver_id)
        return ChatMessage.objects.create(receiver=receiver, **validated_data)


class CallRequestSerializer(serializers.ModelSerializer):
    from_user = PublicUserSerializer(read_only=True)
    to_user = PublicUserSerializer(read_only=True)   # ✅ only output
    to_user_id = serializers.IntegerField(write_only=True)  # ✅ only input

    class Meta:
        model = CallRequest
        fields = ["id", "from_user", "to_user", "to_user_id",
                  "call_type", "accepted", "timestamp"]

    def create(self, validated_data):
        to_user_id = validated_data.pop("to_user_id")
        to_user = User.objects.get(id=to_user_id)
        return CallRequest.objects.create(to_user=to_user, **validated_data)

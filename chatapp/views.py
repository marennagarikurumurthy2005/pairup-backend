from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import ConnectionRequest, ChatMessage, CallRequest
from .serializers import ConnectionRequestSerializer, ChatMessageSerializer, CallRequestSerializer
from users.models import User

# Connection Requests
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_connection_request(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        return Response({"detail": "Cannot connect to yourself"}, status=400)
    conn, created = ConnectionRequest.objects.get_or_create(
        from_user=request.user, to_user=target_user
    )
    serializer = ConnectionRequestSerializer(conn)
    return Response(serializer.data, status=201 if created else 200)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_connection_request(request, request_id):
    conn = get_object_or_404(ConnectionRequest, id=request_id, to_user=request.user)
    conn.accepted = True
    conn.save()
    serializer = ConnectionRequestSerializer(conn)
    return Response(serializer.data)

# Chat Messages
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_message(request):
    serializer = ChatMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(sender=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def message_list(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=target_user)) |
        (Q(sender=target_user) & Q(receiver=request.user))
    ).order_by("timestamp")
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)

# Call Requests
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_call_request(request):
    serializer = CallRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(from_user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_call_request(request, call_id):
    call = get_object_or_404(CallRequest, id=call_id, to_user=request.user)
    call.accepted = True
    call.save()
    serializer = CallRequestSerializer(call)
    return Response(serializer.data)

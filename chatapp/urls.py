from django.urls import path
from .views import send_call_request,accept_call_request,accept_connection_request,send_message,message_list,send_connection_request

urlpatterns = [
    path("connection/send/<int:user_id>/", send_connection_request, name="send-connection"),
    path("connection/accept/<int:request_id>/", accept_connection_request, name="accept-connection"),

    path("messages/send/", send_message, name="send-message"),
    path("messages/<int:user_id>/", message_list, name="list-messages"),

    path("call/send/", send_call_request, name="send-call"),
    path("call/accept/<int:call_id>/", accept_call_request, name="accept-call"),
]

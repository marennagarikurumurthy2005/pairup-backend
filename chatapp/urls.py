from django.urls import path
from .views import SendConnectionRequestView,AcceptConnectionRequestView,SendMessageView, MessageListView,SendCallRequestView,AcceptCallRequestView

urlpatterns = [
    path("connection/send/<int:user_id>/", SendConnectionRequestView.as_view(), name="send-connection"),
    path("connection/accept/<int:request_id>/", AcceptConnectionRequestView.as_view(), name="accept-connection"),

    path("messages/send/", SendMessageView.as_view(), name="send-message"),
    path("messages/<int:user_id>/", MessageListView.as_view(), name="list-messages"),

    path("call/send/", SendCallRequestView.as_view(), name="send-call"),
    path("call/accept/<int:call_id>/", AcceptCallRequestView.as_view(), name="accept-call"),
]

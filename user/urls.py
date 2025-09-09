from django.urls import path
from .views import register_user, login_user, profile,user_list_view

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("profile/", profile, name="profile"),
    path("allusers/", user_list_view, name="all-users"),
]

from django.urls import path
from .views import saved_filter_view,filter_users_view

urlpatterns = [
    path("savedfilter/", saved_filter_view, name="savedfilter"),
    path("setfilters/", filter_users_view, name="setfilters"),
    
]

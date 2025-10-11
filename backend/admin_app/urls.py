from django.urls import path
from .views import admin_ping

urlpatterns = [
    path('ping/', admin_ping),
]

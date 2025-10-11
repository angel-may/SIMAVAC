from django.urls import path
from .views import tutor_ping

urlpatterns = [
    path('ping/', tutor_ping),
]

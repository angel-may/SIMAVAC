from django.urls import path
from .views import doctor_ping

urlpatterns = [
    path('ping/', doctor_ping),
]

from django.urls import path
from .views import enfermera_ping  # ← CORRECTO

urlpatterns = [
    path('ping/', enfermera_ping),
]

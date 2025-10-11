from django.urls import path
from .views import ping
from .views_auth import LoginJWTView, RefreshJWTView, me

urlpatterns = [
    path('ping/', ping),                         # GET
    path('auth/login/', LoginJWTView.as_view()), # POST {username, password}
    path('auth/refresh/', RefreshJWTView.as_view()),  # POST {refresh}
    path('auth/me/', me),                        # GET (Bearer)
]

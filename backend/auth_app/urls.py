# 📁 backend/auth_app/urls.py
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
#from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import LoginView, MeView, RegisterView
from .models import Rol
from .serializers import RolSerializer

# ✅ Usamos nuestra versión personalizada
from .views import CustomTokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView


# ============================================================
# 🔹 RolesView (permite GET público)
# ============================================================
@api_view(["GET"])
@permission_classes([AllowAny])
def roles_view(request):
    """ Devuelve la lista de roles habilitados """
    roles = Rol.objects.filter(estado="habilitado")
    serializer = RolSerializer(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ============================================================
# 🔹 Rutas principales del módulo auth_app
# ============================================================
urlpatterns = [
    # 🟢 Registro de usuario
    path("register/", RegisterView.as_view(), name="register"),

    # 🟢 Listado de roles
    path("roles/", roles_view, name="roles"),

    # 🟢 Login (devuelve JWT y datos del usuario)
    path("login/", LoginView.as_view(), name="login"),

    # 🟢 Refrescar y verificar tokens JWT
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # 🟢 Obtener información del usuario autenticado
    path("me/", MeView.as_view(), name="me"),
]

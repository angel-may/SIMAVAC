from types import SimpleNamespace
from django.db import connection
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from backend.auth_app.custom_auth import CustomJWTAuthentication

from .serializers import RegisterSerializer, LoginSerializer, RolSerializer
from .models import Rol

# ============================================================
# 🧩 CUSTOM JWT AUTHENTICATION (usado globalmente)
# ============================================================

# ============================================================
# 🟢 REGISTRO DE USUARIOS
# ============================================================
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================================
# 🟢 LISTADO DE ROLES (público)
# ============================================================
class RolesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        roles = Rol.objects.filter(estado="habilitado")
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ============================================================
# 🟢 LOGIN SIN MODELO USER (usa JWT + claims personalizados)
# ============================================================
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # ❌ no usar JWT en login

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_input = serializer.validated_data["user"]
        password = serializer.validated_data["password"]

        # 🔍 Buscar usuario en tu estructura personalizada
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT u.password, u.username, u.curp, p.nom, p.app, p.apm, p.correo, r.nombre AS rol
                FROM usuario u
                JOIN persona p ON u.curp = p.curp
                JOIN rol r ON u.rol = r.idrol
                WHERE u.username = %s OR p.correo = %s OR p.curp = %s
                LIMIT 1
                """,
                [user_input, user_input, user_input],
            )
            row = cursor.fetchone()

        if not row:
            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        db_password, username, curp, nom, app, apm, correo, rol = row

        if not check_password(password, db_password):
            return Response(
                {"error": "Contraseña incorrecta"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # ============================================================
        # ✅ Generar tokens JWT personalizados
        # ============================================================
        fake_user_id = abs(hash(curp)) % (10**6)

        refresh = RefreshToken.for_user(SimpleNamespace(id=fake_user_id))
        access = refresh.access_token

        # Claims personalizados
        extra_claims = {
            "user_id": fake_user_id,
            "username": username,
            "curp": curp,
            "rol": rol,
        }

        for k, v in extra_claims.items():
            refresh[k] = v
            access[k] = v

        # ============================================================
        # 🟢 Respuesta exitosa
        # ============================================================
        return Response(
            {
                "message": "Inicio de sesión exitoso",
                "access": str(access),
                "refresh": str(refresh),
                "username": username,
                "nombre": f"{nom} {app or ''} {apm or ''}".strip(),
                "correo": correo,
                "rol": rol,
                "curp": curp,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# 🟢 VISTA /ME (usuario autenticado)
# ============================================================
class MeView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {
            "curp": getattr(user, "curp", None),
            "username": getattr(user, "username", None),
            "rol": getattr(user, "rol", None),
            "is_authenticated": getattr(user, "is_authenticated", False),
        }
        return Response(user_data, status=status.HTTP_200_OK)


# ============================================================
# 🟢 CUSTOM TOKEN REFRESH (no depende de auth_user)
# ============================================================
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Serializer que valida el refresh token sin modelo User.
    Copia los claims personalizados del token anterior.
    """

    def validate(self, attrs):
        refresh = attrs.get("refresh")
        if not refresh:
            raise AuthenticationFailed(_("El campo 'refresh' es obligatorio."))

        try:
            token = RefreshToken(refresh)
        except TokenError:
            raise AuthenticationFailed(_("Refresh token inválido o expirado."))

        data = {"access": str(token.access_token)}

        # Copiar claims personalizados al nuevo access
        for key, value in token.payload.items():
            if key not in ["token_type", "exp", "jti"]:
                data[key] = value

        return data


class CustomTokenRefreshView(TokenViewBase):
    """
    Endpoint para refrescar token sin modelo User real.
    """
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except Exception as e:
            print("⚠️ Error al refrescar token:", e)
            return Response(
                {"detail": "Refresh token inválido o expirado."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

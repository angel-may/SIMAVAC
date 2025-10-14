from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from django.db import connection
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer, RolSerializer
from .models import Rol


# ============================================================
# 🟢 Vista pública: Registro
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
# 🟢 Vista pública: Listado de Roles
# ============================================================
class RolesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        roles = Rol.objects.filter(estado="habilitado")
        serializer = RolSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ============================================================
# 🟢 Vista pública: Login con JWT sin modelo User
# ============================================================
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # ❌ Desactiva autenticación JWT en el login

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_input = serializer.validated_data["user"]
        password = serializer.validated_data["password"]

        # 🔹 Buscar usuario por username, correo o CURP
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

        # 🔹 Validar contraseña con hash de Django
        if not check_password(password, db_password):
            return Response(
                {"error": "Contraseña incorrecta"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # ============================================================
        # ✅ Generar tokens JWT sin usar modelo User
        # ============================================================
        refresh = RefreshToken()  # crea token sin asociar a un modelo User
        access_token = refresh.access_token

        # Datos personalizados (claims)
        claims = {
            "curp": curp,
            "username": username,
            "rol": rol,
        }

        for key, value in claims.items():
            refresh[key] = value
            access_token[key] = value

        # ============================================================
        # 🔹 Respuesta final
        # ============================================================
        return Response(
            {
                "message": "Inicio de sesión exitoso",
                "access": str(access_token),
                "refresh": str(refresh),
                "username": username,
                "nombre": f"{nom} {app or ''} {apm or ''}".strip(),
                "correo": correo,
                "rol": rol,
                "curp": curp,
            },
            status=status.HTTP_200_OK,
        )
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class MeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = {
            "curp": request.user.curp if hasattr(request.user, "curp") else None,
            "username": request.user.username if hasattr(request.user, "username") else None,
        }
        return Response(user_data, status=status.HTTP_200_OK)

from types import SimpleNamespace
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    """
    Autenticación JWT sin depender del modelo auth_user.
    Retorna un usuario temporal basado en los claims del token.
    """

    def get_user(self, validated_token):
        # Extraer claims personalizados
        user_id = validated_token.get("user_id")
        username = validated_token.get("username")
        curp = validated_token.get("curp")
        rol = validated_token.get("rol")

        if not user_id or not username:
            raise AuthenticationFailed("Token inválido o sin identificadores válidos.")

        # ✅ Crear un usuario temporal (sin tocar la base de datos)
        user = SimpleNamespace(
            id=user_id,
            username=username,
            curp=curp,
            rol=rol,
            is_authenticated=True,
            is_active=True,
        )

        return user

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers.auth import MyTokenObtainPairSerializer

class LoginJWTView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer

class RefreshJWTView(TokenRefreshView):
    permission_classes = [AllowAny]

@api_view(['GET'])
def me(request):
    # Requiere Authorization: Bearer <access>
    user = request.user
    groups = list(user.groups.values_list('name', flat=True))
    return Response({
        "ok": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email or '',
            "groups": groups,
            "rol": groups[0] if groups else None
        }
    })

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        groups = list(user.groups.values_list('name', flat=True))
        token['username'] = user.username
        token['email'] = user.email or ''
        token['groups'] = groups
        token['rol'] = groups[0] if groups else None
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        groups = list(user.groups.values_list('name', flat=True))
        data['user'] = {
            "id": user.id,
            "username": user.username,
            "email": user.email or '',
            "groups": groups,
            "rol": groups[0] if groups else None,
        }
        return data

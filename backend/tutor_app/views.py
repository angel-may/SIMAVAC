from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from backend.core.permissions import IsTutorRole

@api_view(['GET'])
@permission_classes([IsTutorRole])
def tutor_ping(_):
    return Response({"ok": True, "service": "tutor"})

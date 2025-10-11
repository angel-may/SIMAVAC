from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from backend.core.permissions import IsDoctorRole

@api_view(['GET'])
@permission_classes([IsDoctorRole])
def doctor_ping(_):
    return Response({"ok": True, "service": "doctor"})

from rest_framework import viewsets
from ..models import RegistroVacunacion
from ..serializers import RegistroVacunacionSerializer


class RegistroVacunacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar el registro de vacunaciones aplicadas a los niños.
    Incluye información de vacuna, personal y punto de aplicación.
    """
    queryset = RegistroVacunacion.objects.all().order_by('idregistro')
    serializer_class = RegistroVacunacionSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
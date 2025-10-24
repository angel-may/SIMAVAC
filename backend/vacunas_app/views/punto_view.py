from rest_framework import viewsets
from ..models import PuntoVacunacion
from ..serializers import PuntoVacunacionSerializer


class PuntoVacunacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para administrar los puntos de vacunación.
    Permite ver, registrar, editar y eliminar puntos.
    """
    queryset = PuntoVacunacion.objects.all().order_by('idpunto')
    serializer_class = PuntoVacunacionSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
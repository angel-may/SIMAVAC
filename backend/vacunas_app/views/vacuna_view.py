from rest_framework import viewsets
from ..models import Vacuna
from ..serializers import VacunaSerializer


class VacunaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar las vacunas registradas en el sistema.
    Permite listar, crear, actualizar y eliminar vacunas.
    """
    queryset = Vacuna.objects.all().order_by('id')
    serializer_class = VacunaSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
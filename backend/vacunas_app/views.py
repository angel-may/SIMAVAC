from rest_framework import viewsets
from .models import Vacuna, PuntoVacunacion, RegistroVacunacion
from .serializers import VacunaSerializer, PuntoVacunacionSerializer, RegistroVacunacionSerializer

# ✅ ViewSet para Vacunas
class VacunaViewSet(viewsets.ModelViewSet):
    queryset = Vacuna.objects.all().order_by('id')
    serializer_class = VacunaSerializer


# ✅ ViewSet para Puntos de Vacunación
class PuntoVacunacionViewSet(viewsets.ModelViewSet):
    queryset = PuntoVacunacion.objects.all().order_by('idpunto')
    serializer_class = PuntoVacunacionSerializer


# ✅ ViewSet para Registro de Vacunación
class RegistroVacunacionViewSet(viewsets.ModelViewSet):
    queryset = RegistroVacunacion.objects.all().order_by('idregistro')
    serializer_class = RegistroVacunacionSerializer
 
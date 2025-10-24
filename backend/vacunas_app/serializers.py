from rest_framework import serializers
from .models import Vacuna, PuntoVacunacion, RegistroVacunacion

class VacunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacuna
        fields = '__all__'


class PuntoVacunacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntoVacunacion
        fields = '__all__'


class RegistroVacunacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroVacunacion
        fields = '__all__'

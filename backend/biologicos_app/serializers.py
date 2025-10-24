# backend/biologicos_app/serializers.py
from rest_framework import serializers
from .models import Biologico, Almacen


# ======================================================
# 🧩 Serializer del Almacén
# ======================================================
class AlmacenSerializer(serializers.ModelSerializer):
    biologico_nombre = serializers.ReadOnlyField(source="biologico.nombre")

    class Meta:
        model = Almacen
        fields = [
            "idalmacen",
            "biologico",
            "biologico_nombre",
            "idunidad",
            "tipo",
            "cantidad",
            "fecha_registro",
            "observaciones",
        ]
        read_only_fields = ["idalmacen", "fecha_registro"]


# ======================================================
# 💉 Serializer del Biológico
# ======================================================
class BiologicoSerializer(serializers.ModelSerializer):
    # 🔹 Si quieres incluir los movimientos (solo lectura)
    movimientos = AlmacenSerializer(many=True, read_only=True)

    class Meta:
        model = Biologico
        fields = [
            "idvacuna",
            "nombre",
            "dosisrequeridas",
            "intervalodias",
            "edadminimameses",
            "edadmaximameses",
            "restricciones",
            "idesquema",
            "movimientos",  # opcional para ver histórico
        ]
        read_only_fields = ["idvacuna"]

    def create(self, validated_data):
        """
        Al crear un biológico:
        - Solo guarda la información base del registro.
        - No requiere manejar cantidades ni almacén aquí, porque tu tabla no lo tiene.
        """
        biologico = super().create(validated_data)
        return biologico

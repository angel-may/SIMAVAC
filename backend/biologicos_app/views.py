# 📁 backend/biologicos_app/views.py
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# ✅ Importamos nuestro autenticador personalizado
from backend.auth_app.custom_auth import CustomJWTAuthentication

from .models import Biologico, Almacen
from .serializers import BiologicoSerializer, AlmacenSerializer
from .permissions import IsAdminOrReadOnly


class BiologicoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de biológicos.
    - Requiere autenticación JWT personalizada.
    - Solo administradores pueden crear, actualizar o eliminar.
    """
    queryset = Biologico.objects.all().order_by("idvacuna")
    serializer_class = BiologicoSerializer

    # ✅ Se usa autenticador que NO depende de auth_user
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "tipo", "fabricante", "lote", "descripcion"]
    ordering_fields = ["created_at", "fecha_caducidad", "cantidad_disponible", "nombre"]

    @action(detail=True, methods=["post"], url_path="mover-a-unidad")
    def mover_a_unidad(self, request, pk=None):
        """
        Mueve una cantidad de biológico desde el almacén general hacia una unidad.
        """
        try:
            biologico = self.get_object()
        except Biologico.DoesNotExist:
            return Response(
                {"detail": "Biológico no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        idunidad = request.data.get("idunidad")
        cantidad = int(request.data.get("cantidad", 0))
        obs = request.data.get("observaciones", "")

        if not idunidad or cantidad <= 0:
            return Response(
                {"detail": "idunidad y cantidad > 0 son requeridos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if biologico.cantidad_disponible < cantidad:
            return Response(
                {"detail": "Cantidad insuficiente en almacén general."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Descontar disponible y registrar movimiento
        biologico.cantidad_disponible -= cantidad
        biologico.save(update_fields=["cantidad_disponible"])

        Almacen.objects.create(
            biologico=biologico,
            idunidad=idunidad,
            tipo="unidad",
            cantidad=cantidad,
            observaciones=obs or f"Movimiento a unidad {idunidad}.",
        )

        return Response(
            {"detail": f"Movimiento de {cantidad} unidades registrado correctamente."},
            status=status.HTTP_200_OK,
        )


class AlmacenViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Solo lectura del histórico de movimientos del almacén.
    """
    queryset = Almacen.objects.select_related("biologico").all().order_by("-fecha_registro")
    serializer_class = AlmacenSerializer

    # ✅ También usa el autenticador personalizado
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["biologico__nombre", "observaciones"]
    ordering_fields = ["fecha_registro", "cantidad", "tipo"]

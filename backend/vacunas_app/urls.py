from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VacunaViewSet, PuntoVacunacionViewSet, RegistroVacunacionViewSet

router = DefaultRouter()
router.register(r'vacunas', VacunaViewSet)
router.register(r'puntos', PuntoVacunacionViewSet)
router.register(r'registros', RegistroVacunacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

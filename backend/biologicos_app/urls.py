from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BiologicoViewSet, AlmacenViewSet

router = DefaultRouter()
router.register(r'biologicos', BiologicoViewSet, basename='biologicos')
router.register(r'almacen', AlmacenViewSet, basename='almacen')

urlpatterns = [
    path('', include(router.urls)),
]

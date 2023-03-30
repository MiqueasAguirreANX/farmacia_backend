from django.urls import path, include
from rest_framework.routers import DefaultRouter
from servicios import viewsets

router = DefaultRouter()
router.register(r"servicios", viewsets.ServicioViewSet, basename="servicios")

urlpatterns = [
    path('', include(router.urls)),
]
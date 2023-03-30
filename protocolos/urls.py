from django.urls import path, include
from rest_framework.routers import DefaultRouter
from protocolos import viewsets
from protocolos.views import ObservacionesOfProtocolo, AddObservacionesToProtocolo

router = DefaultRouter()
router.register(r"protocolos", viewsets.ProtocoloViewSet, basename="protocolos")


urlpatterns = [
    path('', include(router.urls)),
    path(
        'observaciones-of-protocolo/<int:pk>',
        ObservacionesOfProtocolo.as_view(),
        name="observaciones-of-protocolo"
    ),
    path(
        'add-observacion-to-protocolo/<int:pk>',
        AddObservacionesToProtocolo.as_view(),
        name="add-observacion-to-protocolo"
    )
]

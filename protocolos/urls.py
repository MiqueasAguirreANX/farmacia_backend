from django.urls import path, include
from rest_framework.routers import DefaultRouter
from protocolos import viewsets
from protocolos.views import (
    ColaboradoresGananciaView, GananciasMensualesView, MatchedItems, 
    MaximosCompradoresView, ObservacionesOfProtocolo, 
    AddObservacionesToProtocolo, GetProtocolosAbiertosByDateRange, 
    RemoveObservacionesToProtocolo,
)

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
        'matched-items/',
        MatchedItems.as_view(),
        name="matched-items"
    ),
    path(
        'add-observacion-to-protocolo/<int:pk>',
        AddObservacionesToProtocolo.as_view(),
        name="add-observacion-to-protocolo"
    ),
    path(
        'remove-observacion-to-protocolo/<int:pk>/<int:obs_pk>',
        RemoveObservacionesToProtocolo.as_view(),
        name="remove-observacion-to-protocolo"
    ),
    path(
        'get-protocolos-abiertos-by-date-range/<str:date_range>',
        GetProtocolosAbiertosByDateRange.as_view(),
        name="get-protocolos-abiertos-by-date-range"
    ),
    path(
        'colaboradores-ganancias/',
        ColaboradoresGananciaView.as_view(),
        name="colaboradores-ganancias"
    ),
    path(
        'ganancias-mensuales/',
        GananciasMensualesView.as_view(),
        name="ganancias-mensuales"
    ),
    path(
        'maximos-compradores/',
        MaximosCompradoresView.as_view(),
        name="maximos-compradores"
    ),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from observaciones import viewsets
from observaciones.views import GetProtocoloByObservacionWord

router = DefaultRouter()
router.register(r"observaciones", viewsets.ObservacionViewSet, basename="observaciones")

urlpatterns = [
    path(
        "get-protocolo-by-observacion-word",
        GetProtocoloByObservacionWord.as_view(),
        name="get-protocolo-by-observacion-word"
    ),
    path('', include(router.urls)),
]

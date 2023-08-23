from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clientes import viewsets
from clientes.views import GetClienteByNombre, GetClienteByDNI, GetProtocolosDeCliente

router = DefaultRouter()
router.register(r"clientes", viewsets.ClienteViewSet, basename="clientes")

urlpatterns = [
    path('', include(router.urls)),
    path(
        'get-by-nombre/<str:nombre>/<str:apellido>',
        GetClienteByNombre.as_view(),
        name="get-by-nombre"
    ),
    path(
        'get-by-dni/<int:dni>',
        GetClienteByDNI.as_view(),
        name="get-by-dni"
    ),
    path(
        'get-protocolos-de-cliente/<int:cliente>',
        GetProtocolosDeCliente.as_view(),
        name="get-protocolos-de-cliente"
    ),
]
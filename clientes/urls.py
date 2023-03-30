from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clientes import viewsets
from clientes.views import GetClienteByNombre

router = DefaultRouter()
router.register(r"clientes", viewsets.ClienteViewSet, basename="clientes")

urlpatterns = [
    path('', include(router.urls)),
    path(
        'get-by-nombre/<str:nombre>/<str:apellido>',
        GetClienteByNombre.as_view(),
        name="get-by-nombre"
    )
]
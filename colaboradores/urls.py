from django.urls import path, include
from rest_framework.routers import DefaultRouter
from colaboradores import viewsets
from .views import CheckEmpleadoCodigo

router = DefaultRouter()
router.register(r"colaboradores", viewsets.ColaboradorViewSet, basename="colaboradores")

urlpatterns = [
    path('', include(router.urls)),
    path("check-empleado/<str:codigo>", CheckEmpleadoCodigo.as_view(), name="check-empleado"),
]
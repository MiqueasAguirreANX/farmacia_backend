from django.urls import path, include
from rest_framework.routers import DefaultRouter
from observaciones import viewsets

router = DefaultRouter()
router.register(r"observaciones", viewsets.ObservacionViewSet, basename="observaciones")

urlpatterns = [
    path('', include(router.urls)),
]

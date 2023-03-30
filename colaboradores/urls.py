from django.urls import path, include
from rest_framework.routers import DefaultRouter
from colaboradores import viewsets

router = DefaultRouter()
router.register(r"colaboradores", viewsets.ColaboradorViewSet, basename="colaboradores")

urlpatterns = [
    path('', include(router.urls)),
]
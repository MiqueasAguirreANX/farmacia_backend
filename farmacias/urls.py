from django.urls import path, include
from farmacias.views import (
    CurrentFarmacia
)

urlpatterns = [
    path('get-current-farmacia', CurrentFarmacia.as_view(), name="get-current-farmacia"),
]
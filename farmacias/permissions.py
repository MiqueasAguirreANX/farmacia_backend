from rest_framework import permissions
from .models import Farmacia


# class UserPerteneceAFarmacia(permissions.BasePermission):
#     """
#     User belongs to a "farmacia"
#     """

#     def has_permission(self, request):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         farmacia = Farmacia.objects.filter(user=request.user)
#         return farmacia.exists()
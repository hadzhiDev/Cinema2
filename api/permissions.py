from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from pprint import pprint

from apps.models import Movie


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        movie = get_object_or_404(Movie, id=view.kwargs['id'])

        return movie.author == request.user or request.user.is_superuser
    

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):

        return request.user.is_superuser
    

class IsSuperAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):

        return bool(
            request.method in SAFE_METHODS or
            request.user.is_superuser
        )


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
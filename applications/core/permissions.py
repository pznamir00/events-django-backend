from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View  # type:ignore
from applications.core.models import Event


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Event):
        # Read only for everybody
        if request.method in permissions.SAFE_METHODS:
            return True
        # Edit mode only for author (promoter) of event or admin user
        return request.user.is_superuser or obj.promoter == request.user  # type:ignore


class CreateAuthenticatedOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return (not request.method == "POST") or request.user.is_authenticated

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read only for everybody
        if request.method in permissions.SAFE_METHODS:
            return True
        # Edit mode only for author (promoter) of event or admin user
        return request.user.is_superuser or obj.promoter == request.user


class CreateAuthenticatedOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated if request.method == "POST" else True

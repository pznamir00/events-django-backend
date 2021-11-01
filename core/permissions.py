from rest_framework import permissions





class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Allow an access for each user if method is safe (read)
        Otherwise admin rights are required
        """
        return True if request.method in permissions.SAFE_METHODS else request.user.is_superuser
    
    
    
class IsOwnerOrReadOnly(permissions.BasePermission):    
    def has_object_permission(self, request, view, obj):
        """
        Read only for everybody
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        """
        Edit mode only for author (promotor) of event or admin user
        """
        return request.user.is_superuser or obj.promoter == request.user
    
    
    
class CreateAuthenticatedOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated if request.method == 'POST' else True
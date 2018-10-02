from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    """
    Only admin or self allowed
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user
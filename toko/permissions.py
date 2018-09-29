from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    message = 'Allow admin or self'

    def has_object_permission(self, request, view, obj):
        return request.user.id == 1 or obj == request.user
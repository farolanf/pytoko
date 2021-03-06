from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    """
    Only admin or self allowed
    """

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user

class IsAdminOrOwner(permissions.BasePermission):
    """
    Only admin or owner allowed
    """

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user
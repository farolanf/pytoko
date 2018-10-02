from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

class ValidatePasswordMixin(object):

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_password_confirm(self, value):
        if value != self.get_initial().get('password'):
            raise serializers.ValidationError('Kedua password harus sama')
        return value

class ActionPermissionsMixin(object):

    def get_permissions(self):
        """
        Return custom permissions for current action/method.
        """
        if hasattr(self, 'action_permissions'):
            action = self.action if hasattr(self, 'action') \
                    else self.request.method.lower()

            for perm in self.action_permissions:
                if action in perm['actions']:
                    return [permission() for permission in perm['permission_classes']]

        return super().get_permissions()

class FilterFieldsMixin(object):
    """
    Allow filtering fields based on permissions. 
    """
    def get_field_names(self, *args, **kwargs):
        fields = super().get_field_names(*args, **kwargs)

        if self.instance is not None and hasattr(self._context, 'view'):

            # filter based on permissions
            if hasattr(self, 'Meta') and hasattr(self.Meta, 'field_permissions'):
                fields = self.apply_field_permissions(fields)

            # call filter method if defined
            if hasattr(self, 'filter_fields'):
                fields = self.filter_fields(fields)

        return fields

    def apply_field_permissions(self, fields):
        return [field for field in fields if self.field_allowed(field)]

    def field_allowed(self, field):
        return check_permissions(field, 'fields', self.Meta.field_permissions,
                self._context['request'], self._context['view'], self.instance)

    # def filter_fields(self, fields):
    #     # do some filters
    #     # ...
    #     return fields

def check_permissions(name, field_name, permissions, request, view, obj=None):
    for perm in permissions:
        if not name in perm[field_name]: continue
        permissions = [permission() for permission in perm['permission_classes']]
        for permission in permissions:
            if obj is None:
                if not permission.has_permission(request, view):
                    return False
            else:
                if not permission.has_object_permission(request, view, obj):
                    return False
    return True

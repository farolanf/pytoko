import os
from django.db import models
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .permissions import IsAdminOrSelf, IsAdminOrOwner

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

class BrowsePermissionMixin(ActionPermissionsMixin):
    action_permissions = (
        {
            'actions': ['list', 'retrieve'],
            'permission_classes': [],
        },
    )

class UserPermissionMixin(ActionPermissionsMixin):
    action_permissions = (
        {
            'actions': ['retrieve'],
            'permission_classes': [],
        },
        {
            'actions': ['update', 'partial_update'],
            'permission_classes': [IsAdminOrSelf],
        },
    )

class PostPermissionMixin(ActionPermissionsMixin):
    action_permissions = (
        {
            'actions': ['list', 'retrieve'],
            'permission_classes': [],
        },
        {
            'actions': ['create'],
            'permission_classes': [IsAuthenticated],
        },
        {
            'actions': ['update', 'partial_update'],
            'permission_classes': [IsAdminOrOwner],
        },
    )

class ValidatePasswordMixin(object):

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_password_confirm(self, value):
        if value != self.get_initial().get('password'):
            raise serializers.ValidationError('Password tidak sama')
        return value

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

class HtmlModelViewSetMixin:
    renderer_classes = [TemplateHTMLRenderer]
    template_dir = None
    update_success_url = '/'

    def list(self, request):
        """
        Show the list page with objects owned by the user.
        """
        response = super().list(request)
        return Response({
                'data': response.data,
                'paginator': self.paginator,
                'page': self.paginator.page,
            }, 
            template_name=self.get_template_path('list.html'))

    def retrieve(self, *args, **kwargs):
        """
        Show edit form for the object.
        """
        serializer = self.get_serializer(self.get_object())
        return Response({
            'obj': serializer.data,
            'serializer': serializer,
        }, template_name=self.get_template_path('detail.html'))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        valid = serializer.is_valid()

        if valid:
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return redirect(self.update_success_url)

        return Response({
            'obj': instance,
            'serializer': serializer,
        }, template_name=self.get_template_path('detail.html'))

    def get_template_path(self, name):
        return os.path.join(self.template_dir, name)

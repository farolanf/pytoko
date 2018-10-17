import os
from django.db import models
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.status import HTTP_400_BAD_REQUEST
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

class SetFieldLabelsMixin:

    def get_fields(self):
        fields = super().get_fields()
        self.set_field_labels(fields)
        return fields

    def set_field_labels(self, fields):
        if hasattr(self.Meta, 'field_labels'):
            for field_name, field in fields.items():
                field.label = self.Meta.field_labels.get(field_name, field.label)

class HtmlModelViewSetMixin:
    renderer_classes = [TemplateHTMLRenderer]
    template_dir = None
    create_success_url = '/'
    update_success_url = '/'

    def list(self, request):
        """
        Show list page with objects owned by the user.
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
        Show detail page for the object.
        """
        return self.render_detail('detail.html')

    def new(self, *args, **kwargs):
        """
        Show creation form.
        """
        serializer = self.get_serializer()
        return Response({
            'serializer': serializer,
        }, template_name=self.get_template_path('new.html'))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return redirect(self.create_success_url)

        return self.render_object(self.get_new_obj(serializer, request.data), serializer, 'new.html', status=HTTP_400_BAD_REQUEST)

    def edit(self, *args, **kwargs):
        """
        Show edit form for the object get.
        """
        return self.render_detail('edit.html')

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

        return self.render_object(self.get_edit_obj(serializer, instance, request.data), serializer, 'edit.html', status=HTTP_400_BAD_REQUEST)

    def get_new_obj(self, serializer, data):
        obj = {}
        for field in serializer._writable_fields:
            obj[field.field_name] = field.get_value(data)
        return obj

    def get_edit_obj(self, serializer, instance, data):
        obj = serializer.to_representation(instance)
        for field in serializer._writable_fields:
            obj[field.field_name] = field.get_value(data)
        return obj

    def render_detail(self, template):
        serializer = self.get_serializer(self.get_object())
        return self.render_object(serializer.data, serializer, template)

    def render_object(self, obj, serializer, template, status=None):
        return Response({
            'obj': obj,
            'serializer': serializer,
        }, template_name=self.get_template_path(template), status=status)

    def get_template_path(self, name):
        return os.path.join(self.template_dir, name)

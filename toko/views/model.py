from django.shortcuts import render
from django.core import exceptions

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import exception_handler as _exception_handler
from rest_framework.utils.html import parse_html_list, parse_html_dict
from rest_framework import status

from toko import models
from toko import serializers
from toko import mixins
from toko.permissions import IsAdminOrOwner
from toko import pagination

class HtmlModelViewSet(mixins.HtmlModelViewSetMixin, viewsets.ModelViewSet):
    pass

class FileViewSet(mixins.ActionPermissionsMixin, viewsets.ModelViewSet):
    queryset = models.File.objects.all()
    serializer_class = serializers.FilesUploadSerializer
    action_permissions = (
        {
            'actions': ['process'],
            'permission_classes': [IsAuthenticated],
        },
        {
            'actions': ['create', 'update', 'destroy'],
            'permission_classes': [IsAdminOrOwner],
        },
    )

    @action(detail=False, methods=['post'])
    def process(self, request):

        delete = parse_html_list(request.data, 'del')
        add = parse_html_list(request.data, 'add')
        update = parse_html_list(request.data, 'update')

        # delete
        delete_queryset = models.File.objects.filter(pk__in=delete).all()

        for obj in delete_queryset:
            self.check_object_permissions(request, obj)

        delete_queryset.delete()

        errors = {}

        if add:
            serializer = serializers.FileListSerializer(data=add, context={'request': request})

            if serializer.is_valid():
                serializer.save()
                add = serializer.data
            else:
                errors['add'] = serializer.errors

        if update:
            result = []

            for attrs in update:
                obj = models.File.objects.get(pk=attrs['id'])
                self.check_object_permissions(request, obj)

                serializer = serializers.FileSerializer(obj, data=attrs, context={'request': request})

                if serializer.is_valid():
                    serializer.save()
                    result.append(serializer.data)
                else:
                    errors['update'] = errors.get('update', []) 
                    errors['update'].append(serializer.errors)

            update = result

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'add': add,
            'update': update
        })

        
class KabupatenViewSet(mixins.ActionPermissionsMixin, viewsets.ModelViewSet):
    queryset = models.Kabupaten.objects.all()
    serializer_class = serializers.KabupatenSerializer
    action_permissions = (
        {
            'actions': ['list'],
            'permission_classes': [],
        },
    )
    filter_fields = ('provinsi_id',)

class AdViewSet(mixins.ActionPermissionsMixin, HtmlModelViewSet):
    queryset = models.Ad.objects.order_by('-updated_at').all()
    pagination_class = pagination.StandardPagination
    serializer_class = serializers.AdSerializer
    action_permissions = (
        {
            'actions': ['premium', 'info'],
            'permission_classes': [],
        },
        {
            'actions': ['list', 'new', 'create'],
            'permission_classes': [IsAuthenticated],
        },
        {
            'actions': ['retrieve', 'edit', 'update', 'partial_update'],
            'permission_classes': [IsAdminOrOwner],
        },
    )
    template_dir = 'toko/ad'
    create_success_url = 'toko:ad-list'
    update_success_url = 'toko:ad-list'

class ValueViewSet(mixins.ActionPermissionsMixin, viewsets.ModelViewSet):
    queryset = models.Value.objects.all()
    serializer_class = serializers.ValueSerializer
    action_permissions = (
        {
            'actions': ['field'],
            'permission_classes': []
        },
    )

    @action(detail=False)
    def field(self, request):
        """ Get all values in group """
        field_id = request.query_params.get('id')
        field = models.Field.objects.get(pk=field_id)
        objs = models.Value.objects.filter(group=field.group).only('id', 'value')
        serializer = self.get_serializer(objs, many=True)
        return Response(serializer.data)

class ProductTypeViewSet(mixins.ActionPermissionsMixin, viewsets.ModelViewSet):
    queryset = models.ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializer
    action_permissions = (
        {
            'actions': ['list', 'specs'],
            'permission_classes': []
        },
    )
    filter_fields = ('categories',)

    @action(detail=True)
    def specs(self, request, pk=None):
        obj = self.get_object()
        serializer = serializers.FieldListSerializer(obj.specs.all())
        return Response(serializer.data)
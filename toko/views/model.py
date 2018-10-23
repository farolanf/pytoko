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

    # TODO: move to filter backend
    # def get_queryset(self):
    #     queryset = super().get_queryset()

    #     category_id = self.request.query_params.get('category', None)
    #     if category_id:
    #         category = Taxonomy.objects.get(pk=category_id)
    #         categories = category.get_descendants(include_self=True).values_list('id', flat=True)
    #         queryset = queryset.filter(category__in=list(categories))

    #     order = self.request.query_params.get('order', None)
    #     if order:
    #         queryset = queryset.order_by(order)
        
    #     return queryset

    @action(detail=False)
    def premium(self, request):
        """
        Get premium ads.
        """
        # TODO: decide which ads to show
        ad = self.get_queryset().order_by('-updated_at').first()
        serializer = self.get_serializer(ad, context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def info(self, request):

        categories = self.get_queryset().order_by().values_list('category', flat=True).distinct()

        return Response({
            'count': self.get_queryset().count(),
            'categories': categories,
        })

    def filter_queryset(self, queryset):
        
        if self.action == 'list':
            queryset = self.request.user.ads.order_by('-updated_at').all()

        return super().filter_queryset(queryset)
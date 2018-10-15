from django.shortcuts import render
from django.core import exceptions

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import exception_handler as _exception_handler

from toko import models
from toko import serializers
from toko import mixins
from toko import permissions
from toko import pagination

class AdViewSet(mixins.ActionPermissionsMixin, mixins.HtmlModelViewSetMixin, viewsets.ModelViewSet):
    queryset = models.Ad.objects.order_by('-updated_at').all()
    pagination_class = pagination.StandardPagination
    serializer_class = serializers.AdSerializer
    action_permissions = (
        {
            'actions': ['premium', 'info'],
            'permission_classes': [],
        },
        {
            'actions': ['list', 'create'],
            'permission_classes': [IsAuthenticated],
        },
        {
            'actions': ['retrieve', 'update', 'partial_update'],
            'permission_classes': [permissions.IsAdminOrOwner],
        },
    )
    template_dir = 'toko/ad'
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
            queryset = self.request.user.ads.all()

        return super().filter_queryset(queryset)
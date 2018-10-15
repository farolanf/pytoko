import os
import re

from django import forms
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views import generic 
from django.views.generic.edit import FormView
from django.core import exceptions

from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import exception_handler as _exception_handler

from .models import User, Provinsi, Kabupaten, Taxonomy, Ad, AdImage
from . import serializers
from .serializers import PublicUserSerializer, FullUserSerializer, PasswordEmailRequestSerializer, PasswordResetSerializer, RegisterSerializer
from .throttling import PasswordEmailThrottle
from .utils.validation import validate
from .utils.mail import send_mail
from .utils.password import create_password_reset, do_password_reset
from .mixins import ActionPermissionsMixin, UserPermissionMixin, BrowsePermissionMixin, PostPermissionMixin
from .permissions import IsAdminOrOwner
from .pagination import StandardPagination
from .forms import RegisterForm, LoginForm, AdForm

User = get_user_model()

class RegisterView(FormView):
    template_name = 'toko/account/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('toko:register-success')

    def form_valid(self, form):
        username = 'user%s%s' % (get_random_string(3), User.objects.count())
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        User.objects.create_user(username=username, email=email, password=password)
        send_mail('Selamat datang', 'toko/mail/welcome.html', email)
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'toko/account/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse('toko:front'))

def logout_view(request):
    logout(request)
    return redirect('toko:front')

class MyAds(LoginRequiredMixin, generic.ListView):
    model = Ad
    template_name = 'toko/ads/my-ads.html'
    paginate_by = 5

class AdEdit(generic.UpdateView):
    model = Ad
    template_name = 'toko/ads/ad-form.html'
    form_class = AdForm
    success_url = reverse_lazy('toko:my-ads')

#=======================================

def is_admin(request):
    return request.path.startswith('/api/')

class AnonView(views.APIView):
    authentication_classes = ()
    permission_classes = ()

class PasswordEmailView(AnonView):
    throttle_classes = (PasswordEmailThrottle,)

    def post(self, request):
        serializer = PasswordEmailRequestSerializer(data=request.data)
        validate(serializer, 'Tidak dapat memproses reset password.')

        email = serializer.validated_data['email']
        token = create_password_reset(email)
        url = '%sreset-password?t=%s' % (request.build_absolute_uri('/'), token)

        send_mail('Password reset', 'toko/mail/password_reset.html', email, 
                context={'url': url})

        return Response({
            'message': 'Permintaan sedang diproses. Silahkan periksa email anda beberapa saat lagi.'
        })

class PasswordResetView(AnonView):

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        validate(serializer, 'Tidak dapat mereset password.')
        do_password_reset(serializer.validated_data.get('token'),      
                serializer.validated_data.get('password'))
        return Response({
            'message': 'Password telah diubah. Silahkan masuk menggunakan password baru anda.'
        })

class UserViewSet(UserPermissionMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        obj = self.get_object() if self.detail else None 

        # show full data for admin and self
        if self.request.user.is_staff or obj == self.request.user:
            return FullUserSerializer
    
        return PublicUserSerializer

class TaxonomyViewSet(ActionPermissionsMixin, viewsets.ModelViewSet):
    queryset = Taxonomy.objects.all()
    serializer_class = serializers.TaxonomySerializer
    filter_fields = ('slug',)
    action_permissions = (
        {
            'actions': ['list', 'retrieve', 'category'],
            'permission_classes': [],
        },
    )

    @action(detail=False)
    def category(self, request):
        category = self.get_queryset().filter(slug='kategori')
        serializer = self.get_serializer(category, many=True, context={'request': request})
        return Response(serializer.data)

class ProvinsiViewSet(BrowsePermissionMixin, viewsets.ModelViewSet):
    queryset = Provinsi.objects.all()
    serializer_class = serializers.ProvinsiSerializer

class KabupatenViewSet(BrowsePermissionMixin, viewsets.ModelViewSet):
    queryset = Kabupaten.objects.all()
    serializer_class = serializers.KabupatenSerializer
    filter_fields = ('provinsi_id',)

class AdImageViewSet(viewsets.ModelViewSet):
    queryset = AdImage.objects.all()
    pagination_class = StandardPagination
    serializer_class = serializers.AdImageSerializer

class AdViewSet(ActionPermissionsMixin, viewsets.ModelViewSet):
    queryset = Ad.objects.order_by('-updated_at').all()
    pagination_class = StandardPagination
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
            'permission_classes': [IsAdminOrOwner],
        },
    )

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

class UserAdViewSet(HtmlModelViewSetMixin, AdViewSet):
    template_dir = 'toko/ad'

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

def index(request):
    return render(request, 'toko/index.html')

def exception_handler(exc, context):
    request = context['request']
    response = _exception_handler(exc, context)

    if not response:
        return
    
    if response.status_code == 401:
        return render(request, 'toko/401.html')
    elif response.status_code == 403 or isinstance(exc, exceptions.PermissionDenied):
        return render(request, 'toko/403.html')
    elif response.status_code == 404:
        return render(request, 'toko/404.html')
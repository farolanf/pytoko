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
from rest_framework.views import exception_handler as _exception_handler

from toko import models
from toko import serializers
from toko import mixins
from toko import throttling
from toko.utils import validation
from toko.utils import mail
from toko.utils import password
from toko import permissions
from toko import pagination
from toko import forms

User = get_user_model()

class RegisterView(FormView):
    template_name = 'toko/account/register.html'
    form_class = forms.RegisterForm
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
    form_class = forms.LoginForm

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
    model = models.Ad
    template_name = 'toko/ads/my-ads.html'
    paginate_by = 5

class AdEdit(generic.UpdateView):
    model = models.Ad
    template_name = 'toko/ads/ad-form.html'
    form_class = forms.AdForm
    success_url = reverse_lazy('toko:my-ads')

#=======================================

# class AnonView(views.APIView):
#     authentication_classes = ()
#     permission_classes = ()

# class PasswordEmailView(AnonView):
#     throttle_classes = (PasswordEmailThrottle,)

#     def post(self, request):
#         serializer = PasswordEmailRequestSerializer(data=request.data)
#         validate(serializer, 'Tidak dapat memproses reset password.')

#         email = serializer.validated_data['email']
#         token = create_password_reset(email)
#         url = '%sreset-password?t=%s' % (request.build_absolute_uri('/'), token)

#         send_mail('Password reset', 'toko/mail/password_reset.html', email, 
#                 context={'url': url})

#         return Response({
#             'message': 'Permintaan sedang diproses. Silahkan periksa email anda beberapa saat lagi.'
#         })

# class PasswordResetView(AnonView):

#     def post(self, request):
#         serializer = PasswordResetSerializer(data=request.data)
#         validate(serializer, 'Tidak dapat mereset password.')
#         do_password_reset(serializer.validated_data.get('token'),      
#                 serializer.validated_data.get('password'))
#         return Response({
#             'message': 'Password telah diubah. Silahkan masuk menggunakan password baru anda.'
#         })

# Model ViewSets #############################################################

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

def index(request):
    return render(request, 'toko/index.html')

def exception_handler(exc, context):
    request = context['request']

    response = _exception_handler(exc, context)

    if request.path.startswith('/api/'):
        return response

    if not response:
        return
    
    if response.status_code == 401:
        return render(request, 'toko/401.html')
    elif response.status_code == 403 or isinstance(exc, exceptions.PermissionDenied):
        return render(request, 'toko/403.html')
    elif response.status_code == 404:
        return render(request, 'toko/404.html')
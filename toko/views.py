from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated
from .models import User, Provinsi, Kabupaten, Taxonomy, Ad, AdImage
from . import serializers
from .serializers import PublicUserSerializer, FullUserSerializer, PasswordEmailRequestSerializer, PasswordResetSerializer, RegisterSerializer
from .throttling import PasswordEmailThrottle
from .utils.validation import validate
from .utils.mail import send_mail
from .utils.password import create_password_reset, do_password_reset
from .mixins import ActionPermissionsMixin, UserPermissionMixin, BrowsePermissionMixin, PostPermissionMixin
from .permissions import IsAdminOrOwner

User = get_user_model()

class AnonView(views.APIView):
    authentication_classes = ()
    permission_classes = ()

class RegisterView(AnonView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        validate(serializer, 'Pendaftaran akun gagal.')

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        username = 'user_%s%s' % (get_random_string(5), User.objects.count())

        user = User.objects.create(username=username, email=email, password=make_password(password))

        send_mail('Selamat datang', 'toko/mail/welcome.html', email)

        return Response({
            'message': 'Pendaftaran berhasil. Silahkan periksa email anda dan lakukan konfirmasi.',
            'user': FullUserSerializer(user, context={'request': request}).data, 
        })

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
            'actions': ['list', 'retrieve'],
            'permission_classes': [],
        },
    )

    @action(detail=False)
    def category(self, request):
        category = self.get_queryset().filter(slug='kategori')
        serializer = self.get_serializer(category, context=self._context)
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
    serializer_class = serializers.AdImageSerializer

class AdViewSet(ActionPermissionsMixin, viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = serializers.HyperlinkedAdSerializer
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
            'actions': ['update', 'partial_update', 'my'],
            'permission_classes': [IsAdminOrOwner],
        },
    )

    @action(detail=False)
    def my(self, request):
        ads = request.user.ads.all()
        serializer = self.get_serializer(ads, many=True, context=self._context)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.AdSerializer
        return super().get_serializer_class()

def index(request):
    return render(request, 'toko/index.html')
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, authentication_classes, permission_classes, throttle_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.status import *
from .models import User
from .serializers import UserSerializer, PasswordEmailRequestSerializer, PasswordResetSerializer, RegisterSerializer
from .permissions import IsAdminOrSelf
from .mixins import ActionPermissionsMixin
from .throttling import PasswordEmailThrottle
from .utils.validation import validate
from .utils.mail import send_mail
from .utils.password import create_password_reset, do_password_reset

User = get_user_model()

class AnonPostView(views.APIView):
    authentication_classes = ()
    permission_classes = ()

class RegisterView(AnonPostView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        validate(serializer, 'Pendaftaran akun gagal.')

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = User.objects.create(email=email, password=make_password(password))

        return Response({
            'message': 'Pendaftaran berhasil. Silahkan periksa email anda dan lakukan konfirmasi.',
            'user': UserSerializer(user, context={'request': request}).data, 
        })

class PasswordEmailView(AnonPostView):
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

class PasswordResetView(AnonPostView):

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        validate(serializer, 'Tidak dapat mereset password.')
        do_password_reset(serializer.validated_data.get('token'),      
                serializer.validated_data.get('password'))
        return Response({
            'message': 'Password telah diubah. Silahkan masuk menggunakan password baru anda.'
        })

class UserViewSet(ActionPermissionsMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    action_permissions = (
        {
            'actions': ['list', 'create', 'destroy'],
            'permission_classes': [IsAdminUser]
        },
        {
            'actions': ['update', 'partial_update'],
            'permission_classes': [IsAdminOrSelf]
        },
    )

def index(request):
    return render(request, 'toko/index.html')
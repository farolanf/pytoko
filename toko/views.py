from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, authentication_classes, permission_classes, throttle_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.status import *
from .models import User
from .serializers import UserSerializer, PasswordEmailRequestSerializer
from .permissions import IsAdminOrSelf
from .mixins import ActionPermissionsMixin
from .throttling import PasswordEmailThrottle
from .validation import validate
from .mail import send_mail

class AnonPostView(views.APIView):
    authentication_classes = ()
    permission_classes = ()

class PasswordEmailView(AnonPostView):
    throttle_classes = (PasswordEmailThrottle,)

    def post(self, request):
        serializer = PasswordEmailRequestSerializer(data=request.data)
        validate(serializer, 'Tidak dapat memproses password reset.')
        send_mail('Password reset', 'toko/mail/password-reset.html', 
                serializer.validated_data['email'])
        return Response({
            'message': 'Permintaan sedang diproses. Silahkan periksa email anda beberapa saat lagi.'
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
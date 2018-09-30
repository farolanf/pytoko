from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAdminUser
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdminOrSelf
from .mixins import ActionPermissionsMixin

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
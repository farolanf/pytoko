from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAdminUser
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdminOrSelf


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdminOrSelf]
        else:
            return super().get_permissions()
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        """
        Pass request and view objects to serializer for permission checks.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, request=request, view=self)
        return Response(serializer.data)

def index(request):
    return render(request, 'toko/index.html')
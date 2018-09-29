from django.contrib.auth import get_user_model
from rest_framework import serializers
from .mixins import FilterFieldsMixin
from .permissions import IsAdminOrSelf

class UserSerializer(FilterFieldsMixin, serializers.HyperlinkedModelSerializer):
    
    class Meta:    
        model = get_user_model()
        fields = ('id', 'url', 'username', 'email', 'permissions')
        field_permissions = [
            {
                'fields': ['email', 'permissions'],
                'permission_classes': [IsAdminOrSelf],
            }
        ]
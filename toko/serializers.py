from django.contrib.auth import get_user_model
from rest_framework import serializers
from .mixins import FilterFieldsMixin
from .permissions import IsAdminOrSelf

class PasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    password_confirm = serializers.CharField(max_length=255)

    def validate_password_confirm(self, value):
        if value != self.get_initial().get('password'):
            raise serializers.ValidationError('Kedua password harus sama')
        return value

class UserSerializer(FilterFieldsMixin, serializers.HyperlinkedModelSerializer):
    
    class Meta:    
        model = get_user_model()
        fields = ('id', 'url', 'username', 'email', 'permissions')
        field_permissions = [
            {
                'fields': ['email', 'permissions'],
                'permission_classes': [IsAdminOrSelf],
            },
        ]
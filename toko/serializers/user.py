from django.contrib.auth import get_user_model
from rest_framework import serializers
from toko import mixins
from toko import models

User = get_user_model()

class RegisterSerializer(mixins.ValidatePasswordMixin, serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    password_confirm = serializers.CharField(max_length=255)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email sudah terdaftar.')
        return value

class PasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email tidak terdaftar.')
        return value

class PasswordResetSerializer(mixins.ValidatePasswordMixin, serializers.Serializer):
    token = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    password_confirm = serializers.CharField(max_length=255)

    def validate_token(self, value):
        if not PasswordReset.objects.filter(token=value).exists():
            raise serializers.ValidationError('Token tidak terdaftar.')
        return value

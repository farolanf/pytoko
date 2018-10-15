from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from toko.mixins import ValidatePasswordMixin
from toko.validators import validate_unique

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'})

class RegisterSerializer(ValidatePasswordMixin, serializers.Serializer):
    email = serializers.EmailField(max_length=255, validators=[
        validate_unique(User, 'email', 'Email sudah terdaftar'),
    ])
    password = serializers.CharField(max_length=255, style={'input_type': 'password'})
    password_confirm = serializers.CharField(max_length=255, style={'input_type': 'password'})
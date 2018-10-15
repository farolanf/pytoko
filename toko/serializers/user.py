from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, validators=[
        validate_password,
    ])
    password_confirm = serializers.CharField(max_length=255)

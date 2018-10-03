from django.contrib.auth import get_user_model
from rest_framework import serializers
from .mixins import FilterFieldsMixin, ValidatePasswordMixin
from .permissions import IsAdminOrSelf
from .models import PasswordReset, Provinsi, Kabupaten
from . import models

User = get_user_model()

class ProvinsiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Provinsi
        fields = ('id', 'name')

class KabupatenSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Kabupaten
        fields = ('id', 'name', 'provinsi_id')

class RegisterSerializer(ValidatePasswordMixin, serializers.Serializer):
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

class PasswordResetSerializer(ValidatePasswordMixin, serializers.Serializer):
    token = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    password_confirm = serializers.CharField(max_length=255)

    def validate_token(self, value):
        if not PasswordReset.objects.filter(token=value).exists():
            raise serializers.ValidationError('Token tidak terdaftar.')
        return value

class UserSerializer(FilterFieldsMixin, serializers.HyperlinkedModelSerializer):
    
    class Meta:    
        model = User
        fields = ('id', 'url', 'username', 'email', 'permissions')
        field_permissions = [
            {
                'fields': ['email', 'permissions'],
                'permission_classes': [IsAdminOrSelf],
            },
        ]

class TaxonomySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Taxonomy
        fields = ('id', 'name', 'parent_id', 'children')

    def get_children(self, instance):
        return [TaxonomySerializer(item).data for item in instance.get_children()]

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = ('id', 'image')

    def to_internal_value(self, data):
        return super().to_internal_value({'image': data})

class AdSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = models.Ad
        fields = ('id', 'title', 'desc', 'category', 'provinsi', 'kabupaten', 'images')

    def create(self, validated_data):
        images = validated_data.pop('images')
        ad = models.Ad.objects.create(**validated_data)
        for image in images:
            img = models.Image.objects.create(**image)
            img.ad_set.add(ad)
            img.save()
        return ad
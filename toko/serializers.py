from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .mixins import FilterFieldsMixin, ValidatePasswordMixin
from .permissions import IsAdminOrSelf
from .models import PasswordReset, Provinsi, Kabupaten
from . import models
from .utils.file import inc_filename

User = get_user_model()

class ProvinsiSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Provinsi
        fields = ('id', 'url', 'name')

class KabupatenSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Kabupaten
        fields = ('id', 'url', 'name', 'provinsi')

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

class PublicUserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:    
        model = User
        fields = ('id', 'url', 'username')

class FullUserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:    
        model = User
        fields = ('id', 'url', 'username', 'email', 'permissions')

class TaxonomySerializer(serializers.HyperlinkedModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Taxonomy
        fields = ('id', 'url', 'name', 'slug', 'parent_id', 'children')

    def get_children(self, instance):
        return [TaxonomySerializer(item, context=self._context).data for item in instance.get_children()]

class AdImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.AdImage
        fields = ('id', 'url', 'image', 'ad')
        read_only_fields = ('ad',)

    def to_internal_value(self, data):
        """
        Wrap uploaded file in a dict.
        If data is not a dict then assume it's a file object and wrap it.
        """
        if not isinstance(data, dict):
            data = {'image': data}
        return super().to_internal_value(data)

class AdSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    images = AdImageSerializer(many=True)

    class Meta:
        model = models.Ad
        fields = ('id', 'url', 'title', 'desc', 'category', 'provinsi', 'kabupaten', 'images', 'user', 'created_at', 'updated_at')

class HyperlinkedAdSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        view_name='user-detail',
    )
    images = AdImageSerializer(many=True)

    class Meta:
        model = models.Ad
        fields = ('id', 'url', 'title', 'desc', 'category', 'provinsi', 'kabupaten', 'images', 'user', 'created_at', 'updated_at')

class AdCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.CharField(min_length=10, max_length=70)
    desc = serializers.CharField(min_length=20, max_length=4000)
    images = AdImageSerializer(many=True)

    class Meta:
        model = models.Ad
        fields = ('id', 'title', 'desc', 'category', 'provinsi', 'kabupaten', 'images', 'user')

    def create(self, validated_data):
        images = validated_data.pop('images')
        ad = models.Ad.objects.create(**validated_data)
        for image in images:
            image['image'].name = inc_filename(image['image'].name)
            models.AdImage.objects.create(ad=ad, image=image['image'])
        return ad

    def update(self, instance, validated_data):
        images = validated_data.pop('images')

        for key, val in validated_data.items():
            setattr(instance, key, val)
        
        instance.images.all().delete()

        for image in images:
            image['image'].name = inc_filename(image['image'].name)
            models.AdImage.objects.create(ad=instance, image=image['image'])

        instance.save()
        return instance

    def validate_images(self, value):
        if len(value) > 1:
            raise serializers.ValidationError('Jumlah foto melebihi batas (maksimal 8 foto).')
        return value

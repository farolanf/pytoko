from django.urls import reverse
from django.db.models import F
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .mixins import FilterFieldsMixin, ValidatePasswordMixin
from .permissions import IsAdminOrSelf
from . import models
from .utils.file import inc_filename

User = get_user_model()

def get_category_queryset():
    root = models.Taxonomy.objects.get(slug='kategori')
    categories = models.Taxonomy.objects.exclude(pk=root.pk).filter(tree_id=root.tree_id, rght=F('lft') + 1)
    return categories.all()

def get_category_choices():

    def get_display_name(obj):
        names = obj.get_ancestors(include_self=True).values_list('name', flat=True)
        return ' / '.join(names[1:])
    
    root = models.Taxonomy.objects.get(slug='kategori')
    categories = root.get_descendants().filter(rght=F('lft') + 1)
    choices = [(obj.id, get_display_name(obj)) for obj in categories]
    return choices

# Fields #####################################################################


# Input Serializers ##########################################################

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

# Model Serializers ##########################################################

class ProvinsiSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = models.Provinsi
        fields = ('id', 'url', 'name')
        extra_kwargs = {
            'url': {'view_name': 'toko:provinsi-detail'},
        }

class KabupatenSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = models.Kabupaten
        fields = ('id', 'url', 'name', 'provinsi')
        extra_kwargs = {
            'url': {'view_name': 'toko:kabupaten-detail'},
            'provinsi': {'view_name': 'toko:provinsi-detail'},
        }

class PublicUserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:    
        model = User
        fields = ('id', 'url', 'username')
        extra_kwargs = {
            'url': {'view_name': 'toko:user-detail'},
        }

class FullUserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:    
        model = User
        fields = ('id', 'url', 'username', 'email', 'permissions')
        extra_kwargs = {
            'url': {'view_name': 'toko:user-detail'},
        }

class TaxonomySerializer(serializers.HyperlinkedModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Taxonomy
        fields = ('id', 'url', 'name', 'slug', 'parent_id', 'children')
        extra_kwargs = {
            'url': {'view_name': 'toko:taxonomy-detail'},
        }

    def get_children(self, instance):
        return [TaxonomySerializer(item, context=self._context).data for item in instance.get_children()]

class AdImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.AdImage
        fields = ('id', 'url', 'image', 'ad')
        read_only_fields = ('ad',)
        extra_kwargs = {
            'url': {'view_name': 'toko:adimage-detail'},
            'ad': {'view_name': 'toko:ad-detail'},
        }

    def to_internal_value(self, data):
        """
        Wrap uploaded file in a dict.
        If data is not a dict then assume it's a file object and wrap it.
        """
        if not isinstance(data, dict):
            data = {'image': data}
        return super().to_internal_value(data)

class PathHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):

    def use_pk_only_optimization(self):
        return False

    def display_value(self, obj):
        names = obj.get_ancestors(include_self=True).values_list('name', flat=True)
        return ' / '.join(names[1:])

class AdSerializer(serializers.HyperlinkedModelSerializer):
    category = PathHyperlinkedRelatedField(
        queryset=get_category_queryset(),
        view_name='toko:taxonomy-detail'
    )
    
    user = serializers.HyperlinkedRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        view_name='toko:user-detail',
    )
    
    title = serializers.CharField(min_length=10, max_length=70)
    
    desc = serializers.CharField(min_length=20, max_length=4000,
        help_text='Terangkan produk/jasa dengan singkat dan jelas, beserta kekurangannya jika ada.',
        style={
        'base_template': 'textarea.html',
        'rows': 15,
    })

    images = AdImageSerializer(many=True)

    class Meta:
        model = models.Ad
        fields = ('id', 'url', 'category', 'title', 'desc', 'price', 'nego', 'images', 'provinsi', 'kabupaten', 'user', 'created_at', 'updated_at')
        extra_kwargs = {
            'url': {'view_name': 'toko:ad-detail'},
            'category': {'view_name': 'toko:taxonomy-detail'},
            'provinsi': {'view_name': 'toko:provinsi-detail'},
            'kabupaten': {'view_name': 'toko:kabupaten-detail'},
        }

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
        if len(value) > 8:
            raise serializers.ValidationError('Jumlah foto melebihi batas (maksimal 8 foto).')
        return value
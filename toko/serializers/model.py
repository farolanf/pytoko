from django.db.models import F
from django.contrib.auth import get_user_model
from rest_framework import serializers
from toko.mixins import ValidatePasswordMixin
from toko import models
from toko.utils.file import inc_filename

User = get_user_model()

def get_category_queryset():
    root = models.Taxonomy.objects.get(slug='kategori')
    categories = models.Taxonomy.objects.exclude(pk=root.pk).filter(tree_id=root.tree_id, rght=F('lft') + 1)
    return categories.all()

class ProvinsiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Provinsi
        fields = ('id', 'name')

class KabupatenSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Kabupaten
        fields = ('id', 'name', 'provinsi')

class PublicUserSerializer(serializers.ModelSerializer):
    
    class Meta:    
        model = User
        fields = ('id', 'username')

class FullUserSerializer(serializers.ModelSerializer):
    
    class Meta:    
        model = User
        fields = ('id', 'username', 'email', 'permissions')

class TaxonomySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Taxonomy
        fields = ('id', 'name', 'slug', 'parent_id', 'children')

    def get_children(self, instance):
        return [TaxonomySerializer(item, context=self._context).data for item in instance.get_children()]

class AdImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AdImage
        fields = ('id', 'image', 'ad')
        read_only_fields = ('ad',)

    def to_internal_value(self, data):
        """
        Wrap uploaded file in a dict.
        If data is not a dict then assume it's a file object and wrap it.
        """
        if not isinstance(data, dict):
            data = {'image': data}

        return super().to_internal_value(data)

class PathPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def use_pk_only_optimization(self):
        return False

    def display_value(self, obj):
        names = obj.get_ancestors(include_self=True).values_list('name', flat=True)
        return ' / '.join(names[1:])

class AdSerializer(serializers.ModelSerializer):
    category = PathPrimaryKeyRelatedField(queryset=get_category_queryset())
    
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
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
        fields = ('id', 'category', 'title', 'desc', 'price', 'nego', 'images', 'provinsi', 'kabupaten', 'user', 'created_at', 'updated_at')

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
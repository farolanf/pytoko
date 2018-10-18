from django.core.files import File
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers
from toko.mixins import ValidatePasswordMixin, SetFieldLabelsMixin, ExtraItemsMixin
from toko import models
from toko.utils.file import inc_filename
from toko.fields import DynamicQuerysetPrimaryKeyRelatedField, PathPrimaryKeyRelatedField
from toko.querysets import KabupatenDynamicQueryset, get_category_queryset

User = get_user_model()

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
    default_error_messages = {
        'invalid': _('"{input}" not a dict.')
    }

    class Meta:
        model = models.AdImage
        fields = ('id', 'image', 'ad')

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            self.fail('invalid', input=data)
        data['image'].name = inc_filename(data['image'].name)
        return data

class AdImageListSerializer(ExtraItemsMixin, serializers.ListSerializer):
    child = AdImageSerializer()
    extras = 8
    max_length = 8

    def validate(self, attrs):
        if not isinstance(attrs, (list, tuple)):
            raise serializers.ValidationError('Not a list or tuple')
        if len(attrs) > self.max_length:
            raise serializers.ValidationError('Jumlah foto melebihi batas')
        return attrs

class AdSerializer(SetFieldLabelsMixin, serializers.ModelSerializer):
    category = PathPrimaryKeyRelatedField(queryset=get_category_queryset)
    
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    
    title = serializers.CharField(min_length=10, max_length=70)
    
    desc = serializers.CharField(min_length=20, max_length=4000,
        help_text='Terangkan produk/jasa dengan singkat dan jelas, beserta kekurangannya jika ada.',
        style={
        'base_template': 'textarea.html',
        'rows': 15,
    })

    images = AdImageListSerializer(style={'base_template': 'image-uploads.html'})

    kabupaten = DynamicQuerysetPrimaryKeyRelatedField(queryset=KabupatenDynamicQueryset(), with_self=True)

    class Meta:
        model = models.Ad

        fields = ('id', 'category', 'title', 'desc', 'price', 'nego', 'images', 'provinsi', 'kabupaten', 'user', 'created_at', 'updated_at')
        
        field_labels = {
            'category': 'Kategori',
            'title': 'Judul iklan',
            'desc': 'Deskripsi iklan',
            'price': 'Harga',
            'nego': 'Bisa nego',
            'kabupaten': 'Kota',
        }        

    def create(self, validated_data):
        images = validated_data.pop('images')

        instance = super().create(validated_data)

        images = map(lambda file: {'image': file, 'ad': instance}, images)
        self.fields['images'].create(images)

        return instance

    def update(self, instance, validated_data):
        images = validated_data.pop('images')

        super().update(instance, validated_data)

        instance.images.all().delete()
        images = map(lambda file: {'image': file, 'ad': instance}, images)
        self.fields['images'].create(images)

        return instance

    def validate_kabupaten(self, obj):
        provinsi = self.get_initial()['provinsi']
        if obj.provinsi.pk != int(provinsi):
            raise serializers.ValidationError('Kabupaten dan provinsi tidak sesuai')
        return obj
import os
from django.core.files import File
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework.fields import empty
from rest_framework import serializers
from toko.mixins import ValidatePasswordMixin, SetFieldLabelsMixin, ExtraItemsMixin
from toko import models
from toko.utils.file import inc_filename
from toko.fields import DynamicQuerysetPrimaryKeyRelatedField, PathPrimaryKeyRelatedField
from toko.querysets import KabupatenDynamicQueryset, get_category_queryset

User = get_user_model()

class ListSerializer(serializers.ListSerializer):
    min_length = None
    max_length = None
    order = None

    default_error_messages = {
        'not_a_list': _('Expected a list of items but got type "{input_type}".'),
        'min_length': _('Ensure this field has at least {min_length} items.'),
        'max_length': _('Ensure this field has no more than {max_length} items.'),
        'empty': _('This list may not be empty.')
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if self.min_length and len(attrs) < self.min_length:
            self.fail('min_length', min_length=self.min_length)
        if self.max_length and len(attrs) > self.max_length:
            self.fail('max_length', max_length=self.max_length)
        return attrs

    def to_representation(self, data):
        if self.order:
            data = data.order_by(*self.order)
        return super().to_representation(data)

class FileSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'invalid': _('Invalid data. Expected a dictionary or file, but got {datatype} {value}.')
    }

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = models.File
        fields = ('id', 'file', 'user', 'created_at')

    def to_internal_value(self, data):
        if isinstance(data, File):
            data = {'file': data}
        elif not isinstance(data, dict):
            self.fail('invalid', datatype=type(data).__name__, value=data)
        return super().to_internal_value(data)

class FileListSerializer(ExtraItemsMixin, ListSerializer):
    child = FileSerializer()
    min_length = 1
    max_length = 10

class FilesUploadSerializer(serializers.Serializer):

    files = FileListSerializer()

    def create(self, validated_data):
        return {
            'files': self.fields['files'].create(validated_data['files'])
        }

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

class AdImageListSerializer(ExtraItemsMixin, ListSerializer):
    child = FileSerializer()
    extras = 8
    min_length = 0
    max_length = 8
    order = ['adimages__order']

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
            'images': 'Foto',
            'nego': 'Bisa nego',
            'kabupaten': 'Kota',
        }        

    def __init__(self, *args, **kwargs):
        data = kwargs.get('data', empty)
        super().__init__(*args, **kwargs)
        if data is not empty:
            self.fields['images'].child = serializers.IntegerField()

    def create(self, validated_data):
        images = validated_data.pop('images')
        instance = super().create(validated_data)
        self.update_images(images, instance)
        return instance

    def update(self, instance, validated_data):
        images = validated_data.pop('images')
        super().update(instance, validated_data)
        self.update_images(images, instance, remove_others=True)
        return instance

    def update_images(self, images, ad, remove_others=False):

        if remove_others:
            # remove other images
            models.AdImages.objects.filter(ad=ad).exclude(file__in=images).delete()
        
        # update order
        for i, file_id in enumerate(images):
            models.AdImages.objects.update_or_create(ad=ad, file=file_id, defaults={'order': i})

    def validate_kabupaten(self, obj):
        provinsi = self.get_initial()['provinsi']
        if obj.provinsi.pk != int(provinsi):
            raise serializers.ValidationError('Kabupaten dan provinsi tidak sesuai')
        return obj
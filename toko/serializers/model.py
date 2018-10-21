from django.core.files.uploadedfile import UploadedFile
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
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

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.File
        fields = ('id', 'file')

    def to_internal_value(self, data):
        return {'file': data}

class FileListSerializer(ListSerializer):
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

class AdImageSerializer(serializers.ModelSerializer):
    default_error_messages = {
        'invalid': _('"{input}" not a dict.')
    }

    class Meta:
        model = models.AdImage
        fields = ('id', 'image', 'ad')

    def to_internal_value(self, data):
        """
        Convert file id to dict with file obj.
        """
        file = models.File.objects.get(pk=int(data)).file
        return {
            'image': UploadedFile(file, file.name, size=file.size)
        }

class AdImageListSerializer(ExtraItemsMixin, ListSerializer):
    child = AdImageSerializer()
    extras = 8
    max_length = 8

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

    def create(self, validated_data):
        images = validated_data.pop('images')

        instance = super().create(validated_data)
        
        for img in images:
            img['ad'] = instance

        self.fields['images'].create(images)

        return instance

    def update(self, instance, validated_data):
        print(validated_data)
        images = validated_data.pop('images')

        super().update(instance, validated_data)

        instance.images.all().delete()

        for img in images:
            img['ad'] = instance

        self.fields['images'].create(images)

        return instance

    def validate_kabupaten(self, obj):
        provinsi = self.get_initial()['provinsi']
        if obj.provinsi.pk != int(provinsi):
            raise serializers.ValidationError('Kabupaten dan provinsi tidak sesuai')
        return obj
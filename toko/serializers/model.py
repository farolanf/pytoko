import os
import json
from django.core.files import File
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework.fields import empty
from rest_framework import serializers
from toko.mixins import ValidatePasswordMixin, SetFieldLabelsMixin, ExtraItemsMixin
from toko import models
from toko.utils.file import inc_filename
from toko.fields import DynamicQuerysetPrimaryKeyRelatedField, PathPrimaryKeyRelatedField, PathChoicePrimaryKeyRelatedField
from toko.querysets import KabupatenDynamicQueryset, get_category_queryset, ProductTypeDynamicQueryset

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
        elif isinstance(data, dict) and 'id' in data:
            return data
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
    order = ['adimage__order']

class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Field
        fields = ('id', 'group', 'label', 'choices')

class FieldListSerializer(ListSerializer):
    child = FieldSerializer()
    order = ['label']

class SpecSerializer(serializers.ModelSerializer):
    value = serializers.CharField(default='')

    class Meta:
        model = models.FieldValue
        fields = ('id', 'field', 'value')

    def to_representation(self, data):
        ret = super().to_representation(data)
        ret['field'] = data.field.id
        ret['label'] = data.field.label
        ret['value'] = json.loads(data.value.value)
        return ret

class SpecListSerializer(ListSerializer):
    child = SpecSerializer()
    order = ['field__label']

class AdSerializer(SetFieldLabelsMixin, serializers.ModelSerializer):
    category = PathChoicePrimaryKeyRelatedField(queryset=get_category_queryset)
    category_path = PathPrimaryKeyRelatedField(source='category', read_only=True)

    product_type = DynamicQuerysetPrimaryKeyRelatedField(
        source='product.product_type', 
        queryset=ProductTypeDynamicQueryset(),
        with_self=True
    )

    specs = SpecListSerializer(
        source='product.specs',
        style={'base_template': 'specs.html'},
        help_text='Lengkapi spek agar iklan anda mudah ditemukan'
    )

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

        fields = ('id', 'category', 'category_path', 'product_type', 'specs', 'title', 'desc', 'price', 'nego', 'images', 'provinsi', 'kabupaten', 'user', 'created_at', 'updated_at')
        
        field_labels = {
            'category': 'Kategori',
            'product_type': 'Jenis produk',
            'specs': 'Spek',
            'title': 'Judul iklan',
            'desc': 'Deskripsi iklan',
            'price': 'Harga',
            'images': 'Foto',
            'nego': 'Bisa nego',
            'kabupaten': 'Kota',
        }        

    def create(self, validated_data):
        images = validated_data.pop('images')
        product = validated_data.pop('product')

        instance = super().create(validated_data)

        models.Product.objects.create(product_type=product['product_type'], ad=instance)

        self.update_product(instance.product, product)
        self.update_images(images, instance)

        return instance

    def update(self, instance, validated_data):
        images = validated_data.pop('images')
        product = validated_data.pop('product')

        super().update(instance, validated_data)

        self.update_product(instance.product, product)
        self.update_images(images, instance, remove_others=True)

        return instance

    def update_product(self, product, data):
        product.product_type = data['product_type']

        def get_value(field):
            for spec in data['specs']:
                if spec['field'] == field:
                    return json.dumps(spec['value'])
            return json.dumps('')

        for field in product.product_type.specs.all():
            value_json = get_value(field)
            
            value_queryset = models.Value.objects.filter(value__iexact=value_json, group=field.group)
            if value_queryset.exists():
                value = value_queryset.first()
            else:
                value = models.Value.objects.create(
                    group=field.group, value=value_json
                )

            fvalue_queryset = product.specs.filter(field=field)
            if fvalue_queryset.exists():
                fvalue = fvalue_queryset.first()
                fvalue.value = value
                fvalue.save()
            else:
                product.specs.create(
                    product=product, field=field, value=value
                )

        product.specs.exclude(field__in=product.product_type.specs.all()).delete()
        product.save()

    def update_images(self, images, ad, remove_others=False):
        if remove_others:
            # remove other images
            file_ids = [img['id'] for img in images if img['id']]
            models.AdImage.objects.filter(ad=ad).exclude(file_id__in=file_ids).delete()
        
        # update order
        for i, img in enumerate(images):
            if not img['id']: continue
            models.AdImage.objects.update_or_create(ad=ad, file_id=img['id'], defaults={'order': i})

    def validate_kabupaten(self, obj):
        provinsi = self.get_initial()['provinsi']
        if obj.provinsi.pk != int(provinsi):
            raise serializers.ValidationError('Kabupaten dan provinsi tidak sesuai')
        return obj

class ValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Value
        fields = ('id', 'value')

class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductType
        fields = ('id', 'title', 'specs', 'categories')
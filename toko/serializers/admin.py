from django.contrib.auth import get_user_model
from rest_framework import serializers
from toko import models

User = get_user_model()

class AdminUserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:    
        model = User
        fields = ('id', 'url', 'username', 'email', 'permissions')
        extra_kwargs = {
            'url': {'view_name': 'toko:admin-user-detail'},
        }

class AdminFileSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:    
        model = models.File
        fields = ('id', 'url', 'file', 'user', 'created_at')
        extra_kwargs = {
            'url': {'view_name': 'toko:admin-file-detail'},
            'user': {'view_name': 'toko:admin-user-detail'},
        }

class AdminProvinsiSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = models.Provinsi
        fields = ('id', 'url', 'name')
        extra_kwargs = {
            'url': {'view_name': 'toko:admin-provinsi-detail'},
        }

class AdminKabupatenSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = models.Kabupaten
        fields = ('id', 'url', 'name', 'provinsi')
        extra_kwargs = {
            'url': {'view_name': 'toko:admin-kabupaten-detail'},
            'provinsi': {'view_name': 'toko:admin-provinsi-detail'},
        }

class AdminTaxonomySerializer(serializers.HyperlinkedModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Taxonomy
        fields = ('id', 'url', 'name', 'slug', 'product_types', 'parent_id', 'children')
        extra_kwargs = {
            'url': {'view_name': 'toko:admin-taxonomy-detail'},
            'product_types': {'view_name': 'toko:admin-producttype-detail'},
        }

    def get_children(self, instance):
        return [AdminTaxonomySerializer(item, context=self._context).data for item in instance.get_children()]

class AdminValueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Value
        fields = ('id', 'url', 'group', 'value')
        extra_kwargs = {
            'url': {'view_name': 'toko:admin-value-detail'},
            'group': {'view_name': 'toko:admin-value-detail'},
        }

class AdminFieldSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Field
        fields = ('id', 'url', 'group', 'label', 'choices')
        extra_kwargs = {
            'url': {'view_name': 'toko:admin-field-detail'},
            'group': {'view_name': 'toko:admin-value-detail'},
            'choices': {'view_name': 'toko:admin-value-detail'},
        }

class AdminFieldValueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.FieldValue
        fields = ('id', 'url', 'field', 'value')
        extra_kwargs = {
            'url': {'view_name': 'toko:admin-fieldvalue-detail'},
            'field': {'view_name': 'toko:admin-field-detail'},
            'value': {'view_name': 'toko:admin-value-detail'},
        }

class AdminProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = models.ProductType
        fields = ('id', 'url', 'title', 'specs', 'categories')
        extra_kwargs = {
            'url': {'view_name': 'toko:admin-producttype-detail'},
            'specs': {'view_name': 'toko:admin-field-detail'},
            'categories': {'view_name': 'toko:admin-taxonomy-detail'},
        }

class AdminProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Product
        fields = ('id', 'url', 'product_type', 'specs')
        extra_kwargs = {
            'url': {'view_name': 'toko:admin-product-detail'},
            'product_type': {'view_name': 'toko:admin-producttype-detail'},
            'specs': {'view_name': 'toko:admin-fieldvalue-detail'},
        }

class AdminAdSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Ad
        fields = ('id', 'url', 'category', 'title', 'desc', 'price', 'nego', 'images', 'provinsi', 'kabupaten', 'user', 'created_at', 'updated_at')
        extra_kwargs = {
            'url': {'view_name': 'toko:admin-ad-detail'},
            'category': {'view_name': 'toko:admin-taxonomy-detail'},
            'provinsi': {'view_name': 'toko:admin-provinsi-detail'},
            'kabupaten': {'view_name': 'toko:admin-kabupaten-detail'},
            'images': {'view_name': 'toko:admin-adimage-detail'},
            'user': {'view_name': 'toko:admin-user-detail'},
        }
    
class AdminAdImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.AdImage
        fields = ('id', 'url', 'ad', 'file', 'order')
        extra_kwargs = {
            'url': {'view_name': 'toko:admin-adimage-detail'},
            'ad': {'view_name': 'toko:admin-ad-detail'},
            'file': {'view_name': 'toko:admin-file-detail'},
        }
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from toko import models 
from toko import serializers
from toko import permissions
from toko import pagination

User = get_user_model()

class ModelViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.AdminPagination

class AdminFileViewSet(ModelViewSet):
    queryset = models.File.objects.all()
    serializer_class = serializers.AdminFileSerializer

class AdminUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.AdminUserSerializer

class AdminTaxonomyViewSet(ModelViewSet):
    queryset = models.Taxonomy.objects.all()
    serializer_class = serializers.AdminTaxonomySerializer
    filter_fields = ('slug',)

class AdminProvinsiViewSet(ModelViewSet):
    queryset = models.Provinsi.objects.all()
    serializer_class = serializers.AdminProvinsiSerializer

class AdminKabupatenViewSet(ModelViewSet):
    queryset = models.Kabupaten.objects.all()
    serializer_class = serializers.AdminKabupatenSerializer
    filter_fields = ('provinsi_id',)

class AdminValueViewSet(ModelViewSet):
    queryset = models.Value.objects.all()
    serializer_class = serializers.AdminValueSerializer

class AdminFieldViewSet(ModelViewSet):
    queryset = models.Field.objects.all()
    serializer_class = serializers.AdminFieldSerializer

class AdminFieldValueViewSet(ModelViewSet):
    queryset = models.FieldValue.objects.all()
    serializer_class = serializers.AdminFieldValueSerializer

class AdminProductTypeViewSet(ModelViewSet):
    queryset = models.ProductType.objects.all()
    serializer_class = serializers.AdminProductTypeSerializer

class AdminProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.AdminProductSerializer

class AdminAdViewSet(ModelViewSet):
    queryset = models.Ad.objects.order_by('-updated_at').all()
    serializer_class = serializers.AdminAdSerializer

class AdminAdImageViewSet(ModelViewSet):
    queryset = models.AdImage.objects.all()
    serializer_class = serializers.AdminAdImageSerializer
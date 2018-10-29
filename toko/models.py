import re
import json
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from .utils.file import get_upload_path

class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'auth_user'

    @property
    def permissions(self):
        """
        Return a list of permission names.

        It's a combination of groups and specific user permissions.
        """
        group_permissions = [perm.name.lower() for group in self.groups.all()
            for perm in group.permissions.all()]

        return group_permissions

class File(models.Model):
    file = models.FileField(upload_to=get_upload_path, unique=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
   
class Provinsi(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Kabupaten(models.Model):
    name = models.CharField(max_length=100)
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PasswordReset(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField()

class Taxonomy(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Taxonomies'

    class MPTTMeta:
        verbose_name_plural = 'Taxonomies'

    def path_ids_str(self):
        ids = self.get_ancestors(include_self=True).values_list('id', flat=True)
        return '/'.join([str(x) for x in ids])

    def path_name(self):
        names = self.get_ancestors(include_self=True).values_list('name', flat=True)
        return ' / '.join(names[1:])

    def __str__(self):
        return self.path_name()

def group_value_filter():
    return Q(group__value='group') | Q(value='group')

class Value(models.Model):
    group = models.ForeignKey('self', related_name='group_related', null=True, blank=True, on_delete=models.CASCADE, limit_choices_to=group_value_filter)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value

class Field(models.Model):
    group = models.ForeignKey(Value, related_name='field_group_related', on_delete=models.CASCADE, limit_choices_to=group_value_filter)
    label = models.CharField(max_length=50)
    choices = models.ManyToManyField(Value, related_name='choices_parent')

    def __str__(self):
        return self.label

class FieldValue(models.Model):
    field = models.ForeignKey(Field, related_name='values', on_delete=models.CASCADE)
    value = models.ForeignKey(Value, related_name='field_values', on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.field.label, json.loads(self.value.value))

class ProductType(models.Model):
    title = models.CharField(max_length=70)
    specs = models.ManyToManyField(Field, related_name='product_types')
    categories = models.ManyToManyField(Taxonomy, related_name='product_types')

    def __str__(self):
        return self.title

class Product(models.Model):
    product_type = models.ForeignKey(ProductType, related_name='products', on_delete=models.CASCADE)
    specs = models.ManyToManyField(FieldValue, related_name='products')

    def __str__(self):
        return self.product_type.title

class Ad(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='ads', on_delete=models.CASCADE)
    category = models.ForeignKey(Taxonomy, on_delete=models.CASCADE)
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    desc = models.CharField(max_length=4000)
    price = models.IntegerField()
    nego = models.BooleanField()
    images = models.ManyToManyField(File, through='AdImages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, related_name='ads', null=True, on_delete=models.CASCADE)

    def images_url(self):
        return [
            img.file.url
            for img in self.images.all()
        ]

    def suggest(self):
        """ 
        Return every single and double consecutive words from title.
        """
        title = re.sub(r'[^\w\s]', '', self.title)
        words = [
            item
            for item in re.split(r'\s+', title)
            if len(item)
        ]
        inputs = words[:]
        for i, item in enumerate(words):
            if len(words) - i > 1:
                inputs.append(' '.join(words[i:i+2]))
        return inputs

    def __str__(self):
        return self.title

class AdImages(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    order = models.SmallIntegerField()
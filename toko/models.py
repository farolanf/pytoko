import re
from django.db import models
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
    file = models.FileField(upload_to=get_upload_path)
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

    def __str__(self):
        return self.name

class Ad(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='ads', on_delete=models.CASCADE)
    category = models.ForeignKey(Taxonomy, on_delete=models.CASCADE)
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    desc = models.CharField(max_length=4000)
    price = models.IntegerField()
    nego = models.BooleanField()
    images = models.ManyToManyField(File)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
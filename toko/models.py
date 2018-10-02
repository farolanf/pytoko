import re
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

class Provinsi(models.Model):
    name = models.CharField(max_length=100)

class Kabupaten(models.Model):
    name = models.CharField(max_length=100)
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)

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
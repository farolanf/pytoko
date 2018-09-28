from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Taxonomy(MPTTModel):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    class MPTTMeta:
        verbose_name_plural = 'Taxonomies'

    def __str__(self):
        return self.name
from django.db.models import F
from toko import models

def get_category_queryset():
    root = models.Taxonomy.objects.get(slug='kategori')
    categories = models.Taxonomy.objects.exclude(pk=root.pk).filter(tree_id=root.tree_id, rght=F('lft') + 1)
    return categories.all()

class DynamicQueryset:

    def __call__(self, field):
        if hasattr(field.root, 'initial_data'):
            return self.get_input_queryset(field)
        elif field.root.instance:
            return self.get_output_queryset(field)
        return self.get_initial_queryset(field) 

    def get_input_queryset(self, field):
        pass

    def get_output_queryset(self, field):
        pass

    def get_initial_queryset(self, field):
        pass

class KabupatenDynamicQueryset(DynamicQueryset):

    def get_input_queryset(self, field):
        provinsi_id = field.root.get_initial()['provinsi']
        return models.Provinsi.objects.get(pk=provinsi_id).kabupaten_set.all()

    def get_output_queryset(self, field):    
        return field.root.instance.provinsi.kabupaten_set.all()
    
    def get_initial_queryset(self, field):
        return field.root.fields['provinsi'].get_queryset().first().kabupaten_set.all()

class ProductTypeDynamicQueryset(DynamicQueryset):

    def get_input_queryset(self, field):
        category_id = field.root.get_initial()['category']
        return models.Taxonomy.objects.get(pk=category_id).product_types.all()

    def get_output_queryset(self, field):
        return field.root.instance.category.product_types.all()

    def get_initial_queryset(self, field):
        return models.ProductType.objects.all()
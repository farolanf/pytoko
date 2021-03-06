from django_elasticsearch_dsl import DocType, Index, fields
from .models import Ad, Taxonomy, File, Product

ads = Index('ads')
ads.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@ads.doc_type
class AdDocument(DocType):

    category = fields.KeywordField(attr='category.path_name')
    category_path = fields.KeywordField(attr='category.path_ids_str')
    category_slug = fields.KeywordField(attr='category.slug')

    images = fields.ListField(fields.KeywordField(attr='images_url'))

    product = fields.ObjectField(properties={
        'title': fields.KeywordField(attr='product_type.title'),
        'specs': fields.NestedField(attr='specs.all', properties={
            'label': fields.KeywordField(attr='field.label'),
            'value': fields.KeywordField(attr='value.value_json')
        })
    })

    class Meta:
        model = Ad
        fields = [
            'title',
            'desc',
            'price',
            'created_at',
            'updated_at'
        ]
        related_models = [Taxonomy, File, Product]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Taxonomy):
            return related_instance.ad_set.all()
        elif isinstance(related_instance, File):
            return related_instance.ad_set.all()
        elif isinstance(related_instance, Product):
            try:
                return related_instance.ad
            except Ad.DoesNotExist as exc:
                pass

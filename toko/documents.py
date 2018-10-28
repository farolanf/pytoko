from django_elasticsearch_dsl import DocType, Index, fields
from .models import Ad

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

    images = fields.ListField(fields.KeywordField('images_url'))

    class Meta:
        model = Ad
        fields = [
            'title',
            'desc',
            'price'
        ]
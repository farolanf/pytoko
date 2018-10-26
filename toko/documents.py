from elasticsearch_dsl.analysis import analyzer
from django_elasticsearch_dsl import DocType, Index, fields
from .models import Ad

keyword = analyzer('keyword')

ads = Index('ads')
ads.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@ads.doc_type
class AdDocument(DocType):

    suggest = fields.CompletionField()
    category_path = fields.StringField(attr='category.path_str', analyzer=keyword)

    class Meta:
        model = Ad
        fields = [
            'title',
            'desc',
        ]
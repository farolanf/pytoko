from django_elasticsearch_dsl import DocType, Index, fields
from .models import Ad

ad_index = Index('ads')
ad_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@ad_index.doc_type
class AdDocument(DocType):

    suggest = fields.CompletionField()

    class Meta:
        model = Ad
        fields = [
            'title',
            'desc'
        ]
        queryset_pagination = 20
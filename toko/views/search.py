from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from elasticsearch_dsl import Q
from elasticsearch_dsl.analysis import analyzer
from toko.throttling import SearchThrottle
from toko.documents import AdDocument
from toko.serializers import AdSerializer
from toko.models import Ad, Taxonomy
from toko.mixins import ActionPermissionsMixin
from toko.views import HtmlModelViewSet
from toko.pagination import SearchPagination

class SearchViewSet(ActionPermissionsMixin, HtmlModelViewSet):
    queryset = Ad.objects.order_by('-updated_at').all()
    pagination_class = SearchPagination
    serializer_class = AdSerializer
    throttle_classes = [SearchThrottle]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_dir = 'toko/ad'

    action_permissions = (
        {
            'actions': ['list', 'suggest'],
            'permission_classes': [],
        },
    )

    def list(self, request):
        start, end, page_size = self.get_page_info()
        search = AdDocument.search()
        response, serializer = self.paginate_search(search, self.build_query(request))
        end = min(end, response.hits.total)
        return Response({
            'took': response.took,
            'total': response.hits.total,
            'start': start,
            'end': end,
            'paginator': self.paginator,
            'results': serializer.data,
        }, template_name='toko/search.html')

    def build_query(self, request):
        query = request.query_params.get('q', '')
        category_slug = request.query_params.get('category', None)

        if category_slug:
            category_path = Taxonomy.objects.get(slug=category_slug).path_str()
        else:
            category_path = Taxonomy.objects.get(slug='kategori').path_str()

        q = Q({
            'bool': {
                'must': [
                    {
                        'prefix': { 
                            'category_path': category_path
                        }
                    },
                    {
                        'multi_match': {
                            'query': query,
                            'fields': ['title', 'desc']
                        }
                    }
                ]
            }
        })

        return q

    def get_page_num(self):
        return int(self.request.query_params.get('page', 1))

    def get_page_info(self):
        page_size = self.pagination_class.page_size

        page_num = self.get_page_num() 
        start = (page_num - 1) * page_size
        end = start + page_size

        return start, end, page_size

    def paginate_search(self, search, query):
        start, end, page_size = self.get_page_info()
        search = search[start:end].query(query)
        response = search.execute()

        try:      
            self.paginate_queryset(range(response.hits.total))
        except NotFound as exc:
            pass

        serializer = self.get_serializer(search.to_queryset(), many=True)

        return response, serializer

    @action(detail=False)
    def suggest(self, request):
        query = request.query_params.get('q', '')

        data = self.get_suggest(query, completion={
            'field': 'suggest',
            'skip_duplicates': True
        })

        return Response({
            'options': data
        })

    def get_suggest(self, query, **kwargs):

        response = AdDocument.search().suggest('suggestions', query, **kwargs).execute()

        data = [
            {
                'text': opt['text'],
                'category': serializer.instance.category.slug,
                'category_path': serializer.data['category_path'],
            }
            for opt, serializer in
            (
                (opt, AdSerializer(Ad.objects.get(pk=opt['_id'])))
                for opt in response.suggest.suggestions[0].options
            )
        ]

        return data

    def suggest_search(self, query):

        response = AdDocument.search().query(
            Q(
                'match', 
                title={
                    'query': query,
                    'analyzer': analyzer('simple'),
                    'fuzziness': 1
                }
            )
        ).execute()

        data = [
            {
                'text': hit['_source']['title']
            }
            for hit in response.hits.hits
        ]

        return data
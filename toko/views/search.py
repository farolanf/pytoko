from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from elasticsearch_dsl import Q, A
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
        search = self.build_aggregations(search)
        response, serializer = self.paginate_search(search, self.build_query(request))
        end = min(end, response.hits.total)

        categories = response.aggregations.categories.value
        categories.categories = [
            obj
            for key, obj in categories.categories.to_dict().items()
        ]
        categories.categories = sorted(categories.categories, key=lambda x: x.path)

        return Response({
            'query': self.get_query_str(),
            'category_path': self.get_category_path(),
            'took': response.took,
            'total': response.hits.total,
            'start': start,
            'end': end,
            'paginator': self.paginator,
            'results': serializer.data,
            'categories': categories,
        }, template_name='toko/search/search.html')

    def build_aggregations(self, search):
        search.aggs.metric('categories', 'scripted_metric', 
            init_script="""
                params._agg.total = 0;
                params._agg.categories = new HashMap();
                """,
            map_script="""
                params._agg.total++;
                def category = doc.category[0];
                if (!params._agg.categories.containsKey(category)) {
                    def obj = new HashMap();
                    obj.put('count', 1);
                    obj.put('path', category);
                    params._agg.categories.put(category, obj);
                } else {
                    params._agg.categories.get(category).count++;
                }
                """,
            reduce_script="""
                def total = 0;
                def categories = new HashMap();
                for (agg in params._aggs) {
                    total += agg.total;
                    agg.categories.forEach((key, val) -> {
                        if (!categories.containsKey(key)) {
                            categories.put(key, val);
                        } else {
                            categories.get(key).count += val.count;
                        }
                    })
                } 
                def ret = new HashMap();
                ret.put('total', total);
                ret.put('categories', categories);
                return ret
                """
        )
        return search

    def get_query_str(self):
        return self.request.query_params.get('q', '')

    def get_category_path(self):
        category_slug = self.request.query_params.get('category', None)

        if category_slug:
            return Taxonomy.objects.get(slug=category_slug).path_name()

        return 'Semua kategori'

    def build_query(self, request):
        query = self.get_query_str()
        category_slug = request.query_params.get('category', None)

        if category_slug:
            category_path = Taxonomy.objects.get(slug=category_slug).path_ids_str()
        else:
            category_path = Taxonomy.objects.get(slug='kategori').path_ids_str()

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
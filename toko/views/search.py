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

        response = self.paginate_search(search, self.build_query(request))

        end = min(end, response.hits.total)

        categories = response.aggregations.categories.value.to_dict().items()
        categories = sorted(categories, key=lambda x: x[0])

        return Response({
            'query': self.get_query_str(),
            'category_path': self.get_category_path(),
            'took': response.took,
            'total': response.hits.total,
            'start': start,
            'end': end,
            'paginator': self.paginator,
            'results': response.hits.hits,
            'categories': categories,
            'product': response.aggregations.product,
            'prices': self.get_prices()
        }, template_name='toko/search/search.html')

    def get_prices(self):
        return [n for n in range(100000, 500001, 100000)] + \
            [n for n in range(1000000, 5000001, 1000000)]

    def build_aggregations(self, search):
        search.aggs.metric('categories', 'scripted_metric', 
            init_script="""
                params._agg.categories = new HashMap();
                """,
            map_script="""
                def category = doc.category[0];
                if (!params._agg.categories.containsKey(category)) {
                    def obj = new HashMap();
                    obj.put('count', 1);
                    obj.put('slug', doc.category_slug[0]);
                    params._agg.categories.put(category, obj);
                } else {
                    params._agg.categories.get(category).count++;
                }
                """,
            reduce_script="""
                def categories = new HashMap();
                for (agg in params._aggs) {
                    agg.categories.forEach((key, val) -> {
                        if (!categories.containsKey(key)) {
                            categories.put(key, val);
                        } else {
                            categories.get(key).count += val.count;
                        }
                    })
                } 
                return categories
                """
        )

        search.aggs.bucket('product', 'terms', field='product.title') \
            .bucket('specs', 'nested', path='product.specs') \
                .bucket('speclabel', 'terms', field='product.specs.label') \
                    .bucket('specvalue', 'terms', field='product.specs.value')

        return search

    def get_query_str(self):
        return self.request.query_params.get('q', '')

    def get_category_path(self):
        category_slug = self.request.query_params.get('category', None)

        if category_slug:
            return Taxonomy.objects.get(slug=category_slug).path_name()

        return 'Semua kategori'

    def build_query(self, request):
        must = []

        # category filter

        category_slug = request.query_params.get('category', None)

        if category_slug:
            category_path = Taxonomy.objects.get(slug=category_slug).path_ids_str()
        else:
            category_path = Taxonomy.objects.get(slug='kategori').path_ids_str()

        must.append({ 
            'prefix': { 
                'category_path': category_path
            },
        })

        # price filter

        try:
            prices = request.query_params.get('price', '0-0')
            prices = [int(s) for s in prices.split('-')]
            price_from = prices[0]
            price_to = prices[1]
        except:
            price_from = 0
            price_to = 0

        if price_from or price_to:
            must.append({
                'range': {
                    'price': {
                        'gte': price_from,
                        'lte': price_to
                    }
                }
            })

        # query filter

        query = self.get_query_str()

        must.append({
            'bool': {
                'should': self.get_should_query(query)
            }
        })
        
        q = Q({
            'bool': {
                'must': must
            }
        })

        return q

    def get_should_query(self, query):
        should = []

        if query:
            should += [
                {
                    'match_phrase': {
                        'title': query,
                    }
                },
                {
                    'match_phrase': {
                        'desc': query,
                    }
                }
            ]

        return should

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

        return response

    @action(detail=False)
    def suggest(self, request):
        query = request.query_params.get('q', '')

        return Response({
            'options': []
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
import json
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

        search = AdDocument.search().sort(*self.get_sort_args())
        search = self.build_aggregations(search)

        response = self.paginate_search(search, self.build_query())

        end = min(end, response.hits.total)

        response.aggregations.all['key'] = 'Semua'

        response.aggregations.product['buckets'] = [
            response.aggregations.all
        ] + list(response.aggregations.product['buckets'])

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
        }, template_name='toko/search/search.pjax.html')

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

        search.aggs.bucket('all', 'filter', type={'value': 'doc'}) \
            .bucket('specs', 'nested', path='product.specs') \
                .bucket('speclabel', 'terms', field='product.specs.label') \
                    .bucket('specvalue', 'terms', field='product.specs.value')

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

    def build_query(self):
        return Q('bool', must=self.get_must_filter() + self.get_spec_filter())

    def get_sort_args(self):
        sort_type = self.request.query_params.get('sort', 'tersesuai').lower()

        sort = []

        if sort_type == 'termurah':
            sort.append('price')
        elif sort_type == 'termahal':
            sort.append('-price')
        elif sort_type == 'terbaru':
            sort.append('-created_at')
        elif sort_type == 'terlama':
            sort.append('created_at')

        return sort

    def get_must_filter(self):
        must = []

        # query filter

        query = self.get_query_str()
        must.append(self.get_query_filter(query))

        # category filter

        must.append(self.get_category_filter())

        # price filter

        price_query = self.get_price_filter()
        if price_query:
            must.append(price_query)

        return must

    def get_query_filter(self, query):
        should = []

        if query:
            should += [
                {
                    'match_phrase': {
                        'title': {
                            'query': query,
                            'boost': 10
                        }
                    }
                },
                {
                    'match_phrase': {
                        'desc': query,
                    }
                }
            ]

        return Q('bool', should=should)

    def get_category_filter(self):
        category_slug = self.request.query_params.get('category', None)

        if category_slug:
            category_path = Taxonomy.objects.get(slug=category_slug).path_ids_str()
        else:
            category_path = Taxonomy.objects.get(slug='kategori').path_ids_str()

        return Q('prefix', category_path=category_path)

    def get_price_filter(self):
        try:
            prices = self.request.query_params.get('price', '0-0')
            prices = [int(s) for s in prices.split('-')]
            price_from = prices[0]
            price_to = prices[1]
        except:
            price_from = 0
            price_to = 0

        if price_from or price_to:
            return Q('range', price={
                'gte': price_from,
                'lte': price_to
            })

    def get_spec_filter(self):
        products = json.loads(self.request.query_params.get('product', '[]'))
        specs = json.loads(self.request.query_params.get('spec', '{}'))

        products = [Q({
            'terms': {
                'product.title': products
            }
        })] if products else []

        specs_filter = [
            Q('nested', path='product.specs', query={
                'bool': {
                    'must': [
                        {
                            'term': {
                                'product.specs.label': label
                            }
                        },
                        {
                            'terms': {
                                'product.specs.value': values
                            }
                        }
                    ]
                }
            })
            for title, labels in specs.items()
            for label, values in labels.items()
            if title.lower() == 'semua'
        ]

        specs_filter = specs_filter + [
            Q('bool', must=[
                Q({
                    'term': {
                        'product.title': title
                    }
                }),
                Q('nested', path='product.specs', query={
                    'bool': {
                        'must': [
                            {
                                'term': {
                                    'product.specs.label': label
                                }
                            },
                            {
                                'terms': {
                                    'product.specs.value': values
                                }
                            }
                        ]
                    }
                })
            ])
            for title, labels in specs.items()
            for label, values in labels.items()
            if title.lower() != 'semua'
        ] if specs else []

        must = [Q('bool', must=products + specs_filter)] if products or specs_filter else []

        return must

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
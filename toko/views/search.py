from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from elasticsearch_dsl import Q
from toko.throttling import SearchThrottle
from toko.documents import AdDocument

class SearchViewSet(ViewSet):
    authentication_classes = ()
    permission_classes = ()
    throttle_classes = [SearchThrottle]

    def list(self, request):
        return Response('hello')

    @action(detail=False)
    def suggest(self, request):
        query = request.query_params.get('q', '')

        response = AdDocument.search().suggest('suggestions', query, completion={
            'field': 'suggest',
        }).execute()
        
        options = []

        for opt in response.suggest.suggestions[0].options:
            if opt.text not in options:
                options.append(opt.text)

        return Response({
            'options': options
        })
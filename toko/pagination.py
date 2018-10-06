from collections import OrderedDict
from django.core.paginator import Paginator
from rest_framework.pagination import BasePagination
from rest_framework.response import Response

class StandardPagination(BasePagination):
    page_size = 2

    def paginate_queryset(self, queryset, request, view=None):
        page_num = request.query_params.get('page', 1)

        paginator = Paginator(queryset.all(), self.page_size)
        self.page = paginator.page(page_num)

        return self.page.object_list

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('num_pages', self.page.paginator.num_pages),
            ('page_num', self.page.number),
            ('results', data)
        ]))
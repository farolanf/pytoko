from collections import OrderedDict
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardPagination(PageNumberPagination):
    page_size = 20
    template = 'toko/pagination/numbers.html'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page_size', self.page_size),
            ('num_pages', self.page.paginator.num_pages),
            ('page_num', self.page.number),
            ('results', data)
        ]))
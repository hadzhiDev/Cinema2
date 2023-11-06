from rest_framework.pagination import PageNumberPagination


class SimpleResultPagination(PageNumberPagination):
    page_size = 12
    page_query_param = 'page'
    page_size_query_paramv = 'page_size'
    max_page_size = 100
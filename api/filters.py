from django_filters import rest_framework as filters

from apps.models import Movie

class MovieFilter(filters.FilterSet):
    created_at = filters.DateRangeFilter()
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'rating', 'director', 'author', 'year']
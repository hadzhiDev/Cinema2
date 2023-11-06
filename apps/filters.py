import django_filters
from django import forms
from apps.models import Movie, Genre


class MovieFilter(django_filters.FilterSet):

    # data_range = django_filters.DateRangeFilter(field_name='date')
    genres = django_filters.ModelMultipleChoiceFilter(queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Movie
        fields = ('genres', 'director', )
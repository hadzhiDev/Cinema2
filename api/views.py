from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import Http404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404, GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated, SAFE_METHODS, AllowAny
from rest_framework.viewsets import ModelViewSet, ViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework import filters

from api.permissions import IsOwner, IsSuperAdmin, IsSuperAdminOrReadOnly
from api.filters import MovieFilter
from api.paginations import SimpleResultPagination
from api.serializers import GenreSerializer, DirectorSerializer, MovieSerializer, AddUpdateMovieSerializer, UserSerializer
from apps.models import Genre, Director, Movie


class MovieReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    # def get_queryset(self):
    #     id = self.kwargs.get('id')
    #     if not id:
    #         return Movie.objects.all()[:3]
    #     return Movie.objects.filter(id=id)
    
    serializer_class = MovieSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['rating', 'year',]
    search_fields = ['name', 'overview',]
    # filterset_fields = ['genres', 'director', 'author',]
    filterset_class = MovieFilter
    permission_classes = (AllowAny,)

    # @action(methods=['get'], detail=False)
    # def genre(self, request):
    #     genres = Genre.objects.all()
    #     return Response({'genres': [g.name for g in genres]})
    
    # @action(methods=['get'], detail=True)
    # def director(self, request, id):
    #     director = Director.objects.get(id=id)
    #     return Response({'director': director.full_name})


class GenreModelViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = GenreSerializer
    lookup_field = 'id'
    permission_classes = (AllowAny,)


class DirectorModelViewSet(ModelViewSet):
    queryset = Director.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = DirectorSerializer
    lookup_field = 'id'
    permission_classes = (AllowAny,)
    

def fetch_list_genres(request):
    return render(request, 'api/genres.html')


def fetch_list_directors(request):
    return render(request, 'api/directors.html')


def fetch_movies(request):
    return render(request, 'api/movies.html')


@api_view()
@permission_classes((AllowAny,))
def list_users(request):
    users = User.objects.all()
    count = users.count()
    limit = request.GET.get('limit', 6)
    offset = request.GET.get('offset', 1)
    paginator = Paginator(users, limit)
    users = paginator.get_page(offset)
    serializer = UserSerializer(instance=users, many=True)
    response = {
        'count': count,
        'limit': int(limit),
        'offset': int(offset),
        'page_count': paginator.num_pages,
        'data': serializer.data
    }
    return Response(response)


@api_view(['POST'])
def add_movie(request):
    serializer =  AddUpdateMovieSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    movie = serializer.save()
    serializer = AddUpdateMovieSerializer(instance=movie, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def update_movies(request, id):
    movie = get_object_or_404(Movie, id=id)
    serializer =  AddUpdateMovieSerializer(instance=movie, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    movie = serializer.save()
    response_serializer = MovieSerializer(instance=movie, context={'request': request})
    return Response(response_serializer.data)


@api_view(['DELETE'])
@permission_classes((IsOwner, ))
def delete_movies(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.delete()
    return Response({'is_deleted': True}, status=status.HTTP_204_NO_CONTENT)
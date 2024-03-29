from django.urls import path, include

import api.views
from . import views

from rest_framework.routers import DefaultRouter
from .yasg import urlpatterns as url_doc


router = DefaultRouter()
router.register('movies', views.MovieViewSet)
router.register('genres',  views.GenreModelViewSet)
router.register('directors', views.DirectorModelViewSet)
# print(router.urls)

urlpatterns = [
    path('users/', views.list_users),
    # path('genres/fetch/', views.fetch_list_genres),
    # path('directors/fetch/', views.fetch_list_directors),
    # path('movies/fetch/', views.fetch_movies),
    path('auth/', include('api.auth.urls')),

    path('', include(router.urls))
]

urlpatterns += url_doc
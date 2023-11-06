from django.urls import path
from . import views

urlpatterns = [
    path('', views.workspace, name='workspace'),
    path('genres/', views.list_of_genres, name='workspace_genres'),
    path('genres/create/', views.create_genre, name='workspace_create_genre'),
    path('genres/<int:id>/update/', views.update_genre, name='workspace_update_genre'),
    path('genres/<int:id>/delete/', views.delete_genre, name='workspace_delete_genre'),
    path('movies/', views.workspace),
    path('movies/<int:id>', views.detail_movie, name='workspace_detail_movie'),
    path('movies/add', views.add_movie, name='workspace_add_movie'),
    path('movies/<int:id>/update/', views.update_movie, name='workspace_edit_movie'),
    path('movies/<int:id>/delete/', views.delete_movie, name='workspace_delete_movie'),
    path('ajax/comments/<int:id>/delete/', views.delete_comment, name='delete_comment'),
]
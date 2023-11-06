from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('movies/<int:id>/', views.detail, name='detail'),
    path('movies/genre/<int:id>/', views.movies_by_genre, name='movies_by_genre'),
    path('ajax/create_comment/', views.create_comment_ajax, name='create_comment_ajax'),
    path('login/', views.login_profile, name='login'),
    path('logout/', views.logout_profile, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/change_profile/', views.change_profile, name='change_profile'),
    path('profile/change_password/', views.change_password, name='change_password'),

    path('ajax/login/', views.login_ajax, name='login_ajax'),
    path('ajax/logout/', views.logout_ajax, name='logout_ajax'),
]
 
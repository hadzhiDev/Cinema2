from django.contrib import admin
from apps.models import Movie, Genre, Director, Comment

# admin.site.register(Movie)

admin.site.site_header = 'Vilm Cinema'
admin.site.index_title = 'Моя супер админка'

@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin): 
    list_display = ('id', 'name', 'year', 'rating', 'director')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'director')
    list_filter = ('year', 'genres')
    ordering = ['-rating',]
    # list_per_page = 2


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name')
    list_display_links = ('id', 'full_name')
    search_fields = ('id', 'full_name')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'movie', 'date',)
    list_display_links = ('id', 'name',)
    list_filter = ('movie', 'date',)
    search_fields = ('name', 'text',)
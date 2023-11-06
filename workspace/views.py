from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden

from apps.models import Movie, Genre, Director, Comment
from workspace.decorators import required_login_custom


@required_login_custom
def workspace(request):
    movies = Movie.objects.all()
    genre = request.GET.get('genre', None)
    if genre:
        genre = get_object_or_404(Genre, id=int(genre))
        movies = movies.filter(genres=genre)
    genres = Genre.objects.all()
    offset = request.GET.get('offset', 1)
    limit = request.GET.get('limit', 2)
    paginator = Paginator(movies, limit)
    movies = paginator.get_page(offset)
    return render(request, 'workspace/index.html', {'movies_list': movies, 'genres': genres})
    
    
@required_login_custom
def detail_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    comments = Comment.objects.filter(movie=movie)
    offset = request.GET.get('offset', 1)
    limit = request.GET.get('limit', 3)
    paginator = Paginator(comments, limit)
    comments = paginator.get_page(offset)
    genres = Genre.objects.all()
    return render(request, 'workspace/detail.html', {'movie': movie, 'comments': comments, 'genres': genres})


@required_login_custom
def update_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    if request.method == 'POST':
        movie.name = request.POST.get('name')
        movie.overview = request.POST.get('overview')
        movie.rating = request.POST.get('rating')
        movie.year = request.POST.get('year')
        movie.director = Director.objects.get(id=int(request.POST.get('director')))

        image = request.FILES.get('image')
        inner_image = request.FILES.get('inner_image')
        genres = Genre.objects.filter(id__in=list(map(int, request.POST.getlist('genres'))))

        for genre in movie.genres.all():
            movie.genres.remove(genre)

        for genre in genres:
            movie.genres.add(genre)

        if image:
            movieImageSystem = FileSystemStorage('media/images/')
            movieImageSystem.delete(movie.image.name)
            movieImageSystem.save(image.name, image)
            movie.image = image

        if inner_image:
            movieImageSystem1 = FileSystemStorage('media/inner_images/')
            movieImageSystem1.delete(movie.inner_image.name)
            movieImageSystem1.save(inner_image.name, inner_image)
            movie.inner_image = inner_image
        
        movie.save()
        return redirect(f'/workspace/movies/{movie.id}')
    
    genres = Genre.objects.all()
    directors = Director.objects.all()
    return render(request, 'workspace/edit_movie.html', {
        'movie': movie,
        'genres': genres,
        'directors': directors,
    })


@required_login_custom
def add_movie(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        overview = request.POST.get('overview')
        date = timezone.now()
        genres = Genre.objects.filter(id__in=list(map(int, request.POST.getlist('genres'))))
        rating = request.POST.get('rating')
        director = Director.objects.get(id=int(request.POST.get('director')))
        year = request.POST.get('year')
        image = request.FILES.get('image')
        inner_image = request.FILES.get('inner_image')

        movieImageSystem = FileSystemStorage('media/images')
        movieImageSystem.save(image.name, image)
        movieImageSystem2 = FileSystemStorage('media/inner_images')
        movieImageSystem2.save(inner_image.name, inner_image)

        movie = Movie.objects.create(
            name=name,
            overview=overview,
            director=director,
            year=year,
            rating=rating,
            image=image,
            inner_image=inner_image,
        )

        for genre in genres:
            movie.genres.add(genre)
    

        return redirect('/workspace/')

    genres = Genre.objects.all()
    directors = Director.objects.all()
    return render(request, 'workspace/add_movie.html', {
        'genres': genres,
        'directors': directors,
    })


@required_login_custom
def delete_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.delete()
    return redirect('/workspace/')
            

@required_login_custom
def list_of_genres(request):
    genres = Genre.objects.all().order_by('-id')
    offset = request.GET.get('offset', 1)
    limit = request.GET.get('limit', 2)
    paginator = Paginator(genres, limit)
    genres = paginator.get_page(offset)
    return render(request, 'workspace/genres.html', {'genres': genres})
    

@required_login_custom
def create_genre(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        if name is None or name == '':
            return render(request, 'workspace/create_genre.html', {'message': 'Name is required'})
        genre = Genre.objects.create(name=name)
        return redirect('/workspace/genres/')
    return render(request, 'workspace/create_genre.html')


@required_login_custom
def update_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    if request.method == 'POST':
        name = request.POST.get('name', None)
        if name is None or name == '':
            return render(request, 'workspace/edit_genre.html', {
                'message': 'Name is required',
                'genre': genre,
            })
        
        genre.name = name
        genre.save()
        return redirect('/workspace/genres/')
    return render(request, 'workspace/edit_genre.html', {'genre': genre})


@required_login_custom
def delete_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    genre.delete()
    return redirect('/workspace/genres/')


def delete_comment(request, id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return JsonResponse({'isDeleted': True})
    return HttpResponseForbidden()





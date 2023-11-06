from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed

from apps.models import Movie, Genre, Director, Comment
from apps.filters import MovieFilter
from apps.forms import LoginForm
from apps.decorators import increase_views


def main(request):
    search = request.GET.get('search', None)
    if search:
        movies = Movie.objects.filter(name__icontains=search)
        return render(request, 'search_page.html', { 'movies_list': movies,})
    else:
        movies = Movie.objects.all().order_by('-id')
    genre = request.GET.get('genre', None)
    if genre:
        genre = get_object_or_404(Genre, id=int(genre))
        movies = movies.filter(genres=genre)

    filter_set = MovieFilter(request.GET, queryset=movies)

    offset = request.GET.get('offset', 1)
    limit = request.GET.get('limit', 2)
    paginator = Paginator(filter_set.qs, limit)
    movies = paginator.get_page(offset)
    return render(request, 'index.html', { 'movies_list': movies, 'filter': filter_set})


@increase_views
def detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    comments = Comment.objects.filter(movie=movie)
    offset = request.GET.get('offset', 1)
    limit = request.GET.get('limit', 3)
    paginator = Paginator(comments, limit)
    comments = paginator.get_page(offset)
    return render(request, 'detail.html', {'movie': movie, 'comments': comments,})
    


def movies_by_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    movies = Movie.objects.filter(genres=genre)
    return render(request, 'index.html', { 'movies_list': movies, })


def create_comment_ajax(request):
    movie_id = int(request.POST.get('movie'))
    name = request.POST.get('name')
    text = request.POST.get('text')
    movie = get_object_or_404(Movie, id=movie_id)

    new_comment = Comment.objects.create(
        movie=movie,
        name=name,
        text=text,
    )

    return JsonResponse({
        'id': new_comment.id,
        'movie': new_comment.movie.id,
        'name': new_comment.name,
        'text': new_comment.text,
        'date': new_comment.date.strftime('%d %B %Y')
    })


def login_profile(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if request.session.get('next_link', None) is None:
        request.session.modified = True
        request.session['next_link'] = request.GET.get('next') or '/'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                next_link = request.session['next_link']
                return redirect(next_link)
            return render(request, 'auth/login.html', {
                'message': 'The user is not found or invalid password',
                'form': form})
    return render(request, 'auth/login.html', {'form': form})


def logout_profile(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'auth/profile.html')
    return redirect('/')


def change_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            userChecking = User.objects.filter(username=username)

            if userChecking.exists() and request.user.username != username:
                return render(request, 'auth/change_profile.html', {
                    'message': f'User with this username {username} is already exists'
                })
            
            user = request.user
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            user.save()
            return redirect('/profile/')
        return render(request, 'auth/change_profile.html')
    return redirect('/')


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            password = request.POST.get('password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            user = request.user

            if not user.check_password(password):
                return render(request, 'auth/change_password.html', {'message': 'Please enter valid password'})
            if new_password != confirm_password:
                return render(request, 'auth/change_password.html', {'message': 'The passwords don\'t match'})
            if len(new_password) < 8:
                return render(request, 'auth/change_password.html', {
                    'message': 'You password must contain at least 8 charchers'})
            
            user.set_password(new_password)
            user.save()
            login(request, user)
            return redirect('/profile/')
        
        return render(request, 'auth/change_password.html')
    return redirect('/')


def login_ajax(request):
    if request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                
                return JsonResponse({'isAuthenticated': True}, status=200)
            return JsonResponse({'isAuthenticated': False, 'message': 'The user is not found or invalid password',},
                                starus=400)
        if not form.is_valid():
            return JsonResponse({'isAuthenticated': False, 'error': form.errors},
                                starus=400)
    return HttpResponseNotAllowed


def logout_ajax(request):
    if request.user.is_authenticated:
        logout(request)
    return JsonResponse({'isLogout': True}, status=200)


    
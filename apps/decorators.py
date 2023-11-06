from django.shortcuts import get_object_or_404

from apps.models import Movie


def increase_views(func):

    def inner(request, id, *args, **kwargs):
        movie = get_object_or_404(Movie, id=id)
        if request.user.is_authenticated and movie.author.id == request.user.id:
            return func(request, id, *args, **kwargs)
        movie.views += 1
        movie.save()
        return func(request, id, *args, **kwargs)
    
    return inner
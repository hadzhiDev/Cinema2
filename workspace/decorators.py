from django.shortcuts import redirect


def required_login_custom(func):

    def inner_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return redirect('/')
    
    return inner_func
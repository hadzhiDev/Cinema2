from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('login/', views.LoginGenericAPIView.as_view()),
    path('register/', views.RegisterGenericAPIView.as_view()),
    path('api-auth/', include('rest_framework.urls'))
    # path('djoser/', include('djoser.urls')),
    # re_path(r'^djoser/', include('djoser.urls.authtoken')),
]

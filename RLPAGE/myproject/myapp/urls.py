from django.urls import path
from . import views

urlpatterns = [
    path('', views.first, name='first'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('main/', views.main, name='main'),
    path('profile/', views.profile, name='profile'),
]

from django.urls import path, re_path, register_converter
from . import views, converters

urlpatterns = [
    path('', views.index),
    path('welcome', views.welcome),
    path('login', views.login)
]

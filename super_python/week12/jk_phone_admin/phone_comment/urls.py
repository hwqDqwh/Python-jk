from django.urls import path
from . import views


urlpatterns = [
    path('index', views.phone_comment),
]

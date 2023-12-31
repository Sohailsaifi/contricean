# myapp/urls.py
from django.urls import path
from .views import hello, homepage

urlpatterns = [
    path('hello/', hello, name='hello'),
    path('homepage/', homepage, name='homepage'),
]

# myapp/urls.py
from django.urls import path
from .views import homepage, authentication

urlpatterns = [
    path('', homepage, name='homepage'),
    path('authentication/', authentication, name='authentication'),
]

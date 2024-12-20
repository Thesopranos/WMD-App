from django.urls import path
from ..views import render_views

urlpatterns = [
  	path('register/', render_views.register, name='register'),
    path('login/', render_views.login, name='login'),
]

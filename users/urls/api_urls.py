from django.urls import path
from ..views import api_views

urlpatterns = [
  	path('register/', api_views.register, name='register'),
]

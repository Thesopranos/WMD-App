from django.urls import path
from ..views import api_views

urlpatterns = [
  	path('register/', api_views.register, name='register'),
	path('verify/', api_views.verify_code, name='verify'),
]

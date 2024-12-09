from django.urls import path
from . import views

urlpatterns = [
    path('show-all-users', views.show_all_users, name='show-all-users'),
]

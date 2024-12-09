from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser

def show_all_users(request):
    users = CustomUser.objects.all()
    users = [user.username for user in users]
    users = ', '.join(users)
    return HttpResponse(users)

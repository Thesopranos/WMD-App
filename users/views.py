from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser
from django.http import JsonResponse
import json



# !! -- Api for users -- !!
def api_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Geçersiz JSON formatı'}, status=400)

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        dob = data.get('dob')
        notifications = data.get('notifications', False)

        if not username:
            return JsonResponse({'message': 'Kullanıcı adı boş olamaz'}, status=400)

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=firstname,
                last_name=lastname,
                birth_date=dob,
                is_notification_enabled=notifications
            )
            return JsonResponse({'message': 'Kullanıcı başarıyla oluşturuldu'}, status=201)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)


# !! -- Page for users -- !!
def register(request):
    return render(request, 'users/register.html')

def login(request):
    return render(request, 'users/login.html')

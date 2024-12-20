from ..models import CustomUser
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
import string
import random
import json

def register(request):
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

        user_required_fields = ['username', 'email', 'password', 'firstname', 'lastname', 'dob']

        for field in user_required_fields:
            if not data.get(field):
                return JsonResponse({'message': f'{field} alanı boş olamaz', 'success':0}, status=400)

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Kullanıcı adı zaten alınmış', 'success':0}, status=400)
        elif CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'message': 'E-posta zaten alınmış', 'success':0}, status=400)

        verification_code = ''.join(random.choices(string.digits, k=6))

        send_mail(
            subject='E-posta Doğrulama Kodunuz',
            message=f'E-posta doğrulama kodunuz: {verification_code}',
            from_email=None,
            recipient_list=[email],
        )

        cache.set(f'verify_{email}', {
            'username': username,
            'email': email,
            'password': password,
            'firstname': firstname,
            'lastname': lastname,
            'dob': dob,
            'notifications': notifications,
            'code': verification_code
        }, timeout=30000)
        return JsonResponse({'message': 'Kod gönderildi', 'success':1}, status=200)

def verify_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Geçersiz JSON formatı'}, status=400)

        email = data.get('email')
        code = data.get('code')

        if not email or not code:
            return JsonResponse({'message': 'Email ve kod alanları boş olamaz', 'success':0}, status=400)

        cached_data = cache.get(f'verify_{email}')
        if not cached_data:
            return JsonResponse({'message': 'Kod süresi dolmuş veya geçersiz', 'success':0}, status=400)

        if cached_data['code'] != code:
            return JsonResponse({'message': 'Geçersiz kod', 'success':0}, status=400)
        try:
            user = CustomUser.objects.create_user(
                username=cached_data['username'],
                email=cached_data['email'],
                password=cached_data['password'],
                name=cached_data['firstname'],
                surname=cached_data['lastname'],
                birth_date=cached_data['dob'],
                created_at=timezone.now(),
                is_notification_enabled=cached_data['notifications'],
                is_active=True
                )
            user.save()

            return JsonResponse({'message': 'Kullanıcı başarıyla oluşturuldu', 'success':1}, status=201)
        except Exception as e:
                return JsonResponse({'message': str(e), 'success':0}, status=400)
        finally:
                cache.delete(f'verify_{email}')


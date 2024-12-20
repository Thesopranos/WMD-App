from ..models import CustomUser
from django.http import JsonResponse
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

        user_required_fields = ["Kullanıcı adı", "Email", "Şifre", "Ad", "Soyad", "Doğum tarihi"]

        for field in user_required_fields:
            if not locals()[field.lower().replace(' ', '_')]:
                return JsonResponse({'message': f'{field} alanı boş olamaz'}, status=400)

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

# Generated by Django 5.1.4 on 2024-12-20 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_verification'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Verification',
            new_name='VerificationCode',
        ),
    ]

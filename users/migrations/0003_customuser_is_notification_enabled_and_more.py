# Generated by Django 5.1.4 on 2024-12-19 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_obstruct_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_notification_enabled',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='nickname',
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
    ]
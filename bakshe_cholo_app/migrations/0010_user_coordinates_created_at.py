# Generated by Django 4.1 on 2022-09-12 03:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bakshe_cholo_app', '0009_alter_profile_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_coordinates',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

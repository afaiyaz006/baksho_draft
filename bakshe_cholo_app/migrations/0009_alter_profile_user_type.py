# Generated by Django 4.1 on 2022-09-12 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakshe_cholo_app', '0008_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('Regular User', 'Bus Driver'), ('Bus Driver', 'Regular User')], default='Regular User', max_length=100),
        ),
    ]

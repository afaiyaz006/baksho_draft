from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
regularUser='Regular User'
busdriver='Bus Driver'
UserType = [
    (regularUser,'Regular User'),
    (busdriver,'Bus Driver'),
]
class User_Coordinates(models.Model):
    designation=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    lat = models.FloatField(max_length=20)
    lon = models.FloatField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    user_type=models.CharField(max_length=100,choices=UserType,
        default=regularUser)

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Bus(models.Model):
    bus_title=models.CharField(max_length=100)
    bus_route=models.CharField(max_length=200)
    bus_sits=models.IntegerField(blank=True,null=True)
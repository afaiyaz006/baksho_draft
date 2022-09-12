from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
regularUser='ru'
busdriver='bdr'
UserType = [
    (regularUser,'Bus Driver'),
    (busdriver,'Regular User'),
]
class User_Coordinates(models.Model):
    designation=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    lat = models.FloatField(max_length=20)
    lon = models.FloatField(max_length=20)


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    user_type=models.CharField(max_length=100,choices=UserType,
        default=regularUser)

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


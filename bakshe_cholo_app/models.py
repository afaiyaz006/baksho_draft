from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User_Coordinates(models.Model):
    designation=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    lat = models.FloatField(max_length=20)
    lon = models.FloatField(max_length=20)
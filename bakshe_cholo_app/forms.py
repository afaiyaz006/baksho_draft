from django import forms
from django.forms import ModelForm

from .models import User_Coordinates

class UserCoordinatesForm(forms.ModelForm):

      class Meta:
            model = User_Coordinates
            fields= ('lat','lon')
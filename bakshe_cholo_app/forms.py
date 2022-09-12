from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User_Coordinates,UserType,busdriver,regularUser

class SignupForm(UserCreationForm):
    
    userType =forms.ChoiceField(choices=UserType,initial=busdriver)
    class Meta:
        model=User
        fields=('username','userType')
        
class UserCoordinatesForm(forms.ModelForm):

      class Meta:
            model = User_Coordinates
            fields= ('lat','lon')
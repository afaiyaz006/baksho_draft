
from django.urls import path
from . import views

urlpatterns = [
     path('',views.home,name='home'),
     path('maps_form',views.coordinates_form, name = 'coordinates-form'),
     path('map', views.maps, name = 'maps'),
     path('signup',views.signup,name='signup'),
     path('profile',views.profile,name='profile'),
     
]
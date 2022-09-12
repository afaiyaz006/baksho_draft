
from django.shortcuts import render, redirect
from .models import User_Coordinates,Profile
from .forms import *
import folium
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request,'bakshe_cholo_app/home.html')

@login_required
def coordinates_form(request):
    coordinates = User_Coordinates()
    form = UserCoordinatesForm()

    if request.method == 'POST':
       
        form = UserCoordinatesForm(request.POST)
        if form.is_valid():
           print("form is valid")
           coordinates.designation=request.user
           coordinates.lat=form.cleaned_data['lat']
           coordinates.lon=form.cleaned_data['lon']
           coordinates.save()
        return redirect("maps")
    context = {
        'coordinates': coordinates,
        'form' : form,
    }
    return render(request, 'bakshe_cholo_app/maps_form.html', context)
    
@login_required
def maps(request):
    coordinates = list(User_Coordinates.objects.filter(designation=request.user))[0]
    coordinates=[coordinates.lon,coordinates.lat]
    print(coordinates)
    map = folium.Map(coordinates)
    folium.Marker(coordinates).add_to(map)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(map)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(map)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(map)
    folium.LayerControl().add_to(map)


    map = map._repr_html_()
    context = {
      'map': map,

    }
    return render(request, 'bakshe_cholo_app/maps.html', context)


def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.refresh_from_db()
            user.profile.user_type=form.cleaned_data.get('userType')
        
            user.save()
            raw_password=form.cleaned_data.get('password1')
            user = authenticate(username=user.username,password=raw_password)
            login(request,user)
            return redirect('/')
    else:
        
        form=SignupForm()
        
    return render(request,'registration/signup.html',{'form':form})
def profile(request):
    '''
    profile view
    '''
    return render(request,'registration/profile.html')
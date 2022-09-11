
from django.shortcuts import render, redirect
from .models import User_Coordinates
from .forms import *
import folium
# Create your views here.
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

def maps(request):
    coordinates = list(User_Coordinates.objects.filter(designation=request.user))[-1]
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
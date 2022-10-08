
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
    '''
    This is hugely unoptimized  as the coordinates are stored multiple times in multiple instance
    will change it later.
    '''
    
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
    
    '''
    grab latest submitted user coordinate of the currently logged in user and show the recent 5 coordinate as recent position
    '''
    recent_coordinates=User_Coordinates.objects.filter(designation=request.user).order_by('-created_at')
    recent_coordinates=recent_coordinates[:5]
    context = {
        'coordinates': recent_coordinates,
        'form' : form,
    }

    return render(request, 'bakshe_cholo_app/maps_form.html', context)
    
@login_required
def maps(request):

    ### bus driver locations will be added here....
    bus_drivers=Profile.objects.filter(user_type='Bus Driver')
    drivers_coordinates=[]
    for driver in bus_drivers:
        loc=User_Coordinates.objects.filter(designation=driver.user).latest('created_at')
        if loc:
            coord=[loc.lon,loc.lat]
            drivers_coordinates.append(coord)
        
    coordinates = User_Coordinates.objects.filter(designation=request.user).latest('created_at') # get latest location submitted by user
    coordinates=[coordinates.lon,coordinates.lat]
    #print(coordinates)
    
    map = folium.Map(coordinates)

    user_tooltip="User tooltip"
    bus_tooltip="Bus Tooltip"

    #coordinate for destination
    destination_coordinate=[90,23.2929392]
    folium.Marker(destination_coordinate,draggable=True,icon=folium.Icon(color="purple")).add_to(map)
    


    #user coordinate
    folium.Marker(coordinates,popup="👤<i>User</i>", tooltip=user_tooltip,icon=folium.Icon(color="blue")).add_to(map) 
   
   
    #adding driver coordinate
    counter=1
    for coord in drivers_coordinates:

        folium.Marker(coord,popup="🚌<i> BusDriver"+str(counter)+" </i>",tooltip=bus_tooltip,icon=folium.Icon(color="red")).add_to(map)
        folium.PolyLine(locations=[coord,coordinates], color='red').add_to(map)
        counter+=1
    
    
    
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

from django.shortcuts import render, redirect
from .models import User_Coordinates,Profile,Bus
from .forms import *
import folium
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from .location_engine import LocationWorker
location_worker=LocationWorker('walk','time')
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
            coord=(loc.lat,loc.lon)
            drivers_coordinates.append(coord)
        
    coordinates = User_Coordinates.objects.filter(designation=request.user).latest('created_at') # get latest location submitted by user
    user_coordinates=(coordinates.lat,coordinates.lon)
    #print(coordinates)
    shortest_routes=[]
    for driver_coordinate in drivers_coordinates:
        shortest_route=location_worker.calculate_shorted_distance(driver_coordinate,user_coordinates)
        shortest_routes.append(shortest_route)
    print(shortest_routes)
    map=location_worker.make_route(shortest_routes)
    
    user_tooltip="User tooltip"
    bus_tooltip="Bus Tooltip"
    
    #user coordinate
    folium.Marker([user_coordinates[1],user_coordinates[0]],popup="👤<i>User</i>", tooltip=user_tooltip,icon=folium.Icon(color="blue")).add_to(map) 
   
   
    #adding driver coordinate
    counter=1
    for coord in drivers_coordinates:

        folium.Marker([coord[1],coord[0]],popup="🚌<i> BusDriver"+str(counter)+" </i>",tooltip=bus_tooltip,icon=folium.Icon(color="red")).add_to(map)
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

def searchView(request):
    if request.GET:
        search_query=request.GET['sq']
        buses=Bus.objects.filter(bus_title__icontains=search_query)
        return render(request,'bakshe_cholo_app/search.html',{'buses':buses})
    else:
        return render(request,'bakshe_cholo_app/search.html')
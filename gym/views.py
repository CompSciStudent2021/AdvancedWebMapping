import json
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import GymLocation, Profile
from django.core.serializers import serialize

User = get_user_model()

def set_user_location(user_id, latitude, longitude):
    user = User.objects.get(id=user_id)
    location = Point(longitude, latitude)  # Point takes (longitude, latitude)

    # Create or update the user's profile
    profile, created = Profile.objects.get_or_create(user=user)
    profile.location = location
    profile.save()

    return profile

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('gym_map')  # Redirect to the main map view for gyms
    else:
        form = AuthenticationForm()
    return render(request, 'gym/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('gym_login')  # Redirect to the login page after logout

def map_view(request):
    """
    Renders the map view with gym locations.
    """
    gyms = GymLocation.objects.all()
    gyms_json = serialize('geojson', gyms)  # Serialize gym data to GeoJSON

    # Check if user is authenticated before accessing username
    username = request.user.username if request.user.is_authenticated else None

    return render(request, 'gym/map.html', {
        'gym_data': gyms_json,
        'username': username  # Pass username in the same dictionary
    })

def update_location(request):
    if request.method == 'POST' and request.user.is_authenticated:
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if latitude and longitude:
            try:
                latitude = float(latitude)
                longitude = float(longitude)
                location = Point(longitude, latitude)

                # Create or update the user's profile
                profile, created = Profile.objects.get_or_create(user=request.user)
                profile.location = location
                profile.save()

                return JsonResponse({'success': True})
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid coordinates'})
        else:
            return JsonResponse({'success': False, 'error': 'Missing coordinates'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method or user not authenticated'})

def gym_data(request):
    """
    Returns all gym data as JSON.
    """
    gyms = GymLocation.objects.all()  # Get all gym locations
    gym_data = serialize('geojson', gyms)  # Serialize to GeoJSON format
    return JsonResponse(gym_data, safe=False)  # Return as JSON response

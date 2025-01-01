import json
from django.contrib.gis.geos import Point
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm
from .models import GymLocation, Profile
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import RegistrationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import GymLocation
from .serializers import GymLocationSerializer
from .utils import fetch_osm_gyms, fetch_osm_locations
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

def osm_locations_view(request):
    location_type = request.GET.get('type', 'fitness_centre')
    bbox = (51.0, -10.0, 55.5, -5.5)  # Bounding box for Ireland

    try:
        locations = fetch_osm_locations(location_type, bbox)
        if not isinstance(locations, list):  # Ensure the response is a list
            return JsonResponse({"error": "Invalid data format from API"}, status=500)

        return JsonResponse(locations, safe=False)
    except Exception as e:
        print(f"Error in osm_locations_view: {e}")
        return JsonResponse({"error": str(e)}, status=500)


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

def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('gym_map')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Validate the password using Django's built-in validators
                validate_password(form.cleaned_data['password1'], user=None)

                # Save the user
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('gym_map')
            except ValidationError as e:
                # Add password validation errors to the form's non-field errors
                form.add_error(None, e.messages)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, 'gym/registration.html', {'form': form})



def map_view(request):
    """
    Renders the map view with gym locations, including Overpass API data.
    """
    # Fetch gyms from Overpass API
    bbox = (50.0, -10.0, 56.0, -5.0)  # Bounding box for Ireland
    osm_gyms = fetch_osm_gyms(bbox)

    # Existing gyms from your database
    gyms = GymLocation.objects.all()
    gyms_json = serialize('geojson', gyms)  # Serialize gym data to GeoJSON

    # Check if user is authenticated before accessing username
    username = request.user.username if request.user.is_authenticated else None

    return render(request, 'gym/map.html', {
        'gym_data': gyms_json,
        'osm_gyms': osm_gyms,  # Pass Overpass API gyms to the template
        'username': username,
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

class GymLocationList(APIView):
    def get(self, request):
        try:
            gyms = GymLocation.objects.all()
            print(f"Gyms Queryset: {gyms}")  # Debug: Print queryset
            serializer = GymLocationSerializer(gyms, many=True)
            print(f"Serialized Data: {serializer.data}")  # Debug: Print serialized data
            return Response(serializer.data)
        except Exception as e:
            print(f"Error: {e}")  # Debug: Print the error
            return Response({"error": str(e)}, status=500)
from django.contrib.gis import admin
from .models import GymLocation

# Register the TennisCourt model using GISModelAdmin for geospatial features
admin.site.register(GymLocation, admin.GISModelAdmin)
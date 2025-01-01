from rest_framework import serializers
from .models import GymLocation

class GymLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymLocation
        fields = ['id', 'objectid', 'location', 'type', 'itm_x', 'itm_y', 'point']  # Match model fields

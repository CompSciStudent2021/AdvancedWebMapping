from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class GymLocation(models.Model):
    objectid = models.IntegerField(unique=True)  # Store OBJECTID
    location = models.CharField(max_length=100)  # Store Location name
    type = models.CharField(max_length=50)  # Store Type (e.g., exercise stations)
    itm_x = models.FloatField(null=True, blank=True)  # ITM_X coordinate
    itm_y = models.FloatField(null=True, blank=True)  # ITM_Y coordinate
    point = models.PointField()  # Store location as a geographic point (latitude/longitude)

    def __str__(self):
        return self.location  # Corrected to return location name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="gym_profile")
    location = models.PointField(null=True, blank=True)

    def __str__(self):
        return self.user.username
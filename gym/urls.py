"""geodjango_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .views import GymLocationList
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('map/', views.map_view, name='gym_map'),
    path('update_location/', views.update_location, name='update_location'),
    path('login/', views.login_view, name='gym_login'),
    path('logout/', views.logout_view, name='gym_logout'),
    path('gym_data/', views.gym_data, name='gym_data'),  # Add this line for the gym_data endpoint
    path('register/', views.register_view, name='gym_register'),
    path('api/gyms/', GymLocationList.as_view(), name='gym_location_list'),
    path('api/osm-locations/', views.osm_locations_view, name='osm_locations'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
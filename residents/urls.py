from django.urls import path
from . import views

# Routing configurations for the Residents app. 
# These are mapped under the /residents/ prefix in the root urls.py
urlpatterns = [
    # Admin directory tool
    path('directory/', views.resident_directory_view, name='resident_directory'),
    path('onboard/<int:user_id>/', views.onboard_resident_view, name='onboard_resident'),
    
    # Resident personal dashboard
    path('dashboard/', views.resident_dashboard_data_view, name='resident_dashboard_data'),
    
    # Resident data management
    path('family/add/', views.add_family_member_view, name='add_family_member'),
    path('vehicle/add/', views.add_vehicle_view, name='add_vehicle'),
]

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import services
from .models import ResidentProfile

# --- Admin Views ---

@login_required
def resident_directory_view(request):
    """
    Admin-only view that displays a directory of all registered residents.
    Supports searching by name/email and filtering by building.
    """
    # Enforce role-based access control (only admins can view the directory)
    if request.user.role != 'admin':
        return redirect('resident_dashboard')
        
    query = request.GET.get('q') # Search term from URL parameter ?q=...
    building_id = request.GET.get('building') # Building filter
    
    if query:
        # Search residents using our service layer logic
        residents = services.search_resident(query)
    else:
        # List all residents, optionally applying the building filter
        residents = services.list_residents(building_id=building_id)
        
    context = {'residents': residents}
    return render(request, 'residents/directory.html', context)


# --- Resident Views ---

@login_required
def resident_dashboard_data_view(request):
    """
    The personal dashboard for logged-in residents. 
    Displays their flat details, connected family members, and registered vehicles.
    """
    # Block admins or security guards from accessing a resident's personal dashboard
    if request.user.role != 'resident':
        return redirect('admin_dashboard')
        
    try:
        # Fetch the aggregated context data via the service layer
        dashboard_data = services.get_resident_dashboard_data(request.user.id)
    except Exception:
        # If the user is a resident but their profile hasn't been created yet
        dashboard_data = {'error': 'Profile not setup yet. Please contact the administrator.'}
        
    return render(request, 'residents/dashboard.html', dashboard_data)

@login_required
def add_family_member_view(request):
    """
    Provides a form for residents to add new family members to their profile.
    Handles the POST submission to save the new member to the database.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        relation = request.POST.get('relation')
        phone = request.POST.get('phone')
        
        # Link the new family member to the currently logged-in user's profile
        profile = get_object_or_404(ResidentProfile, user=request.user)
        services.add_family_member(profile.id, name, relation, phone)
        
        # Send them back to their dashboard once saved
        return redirect('resident_dashboard_data')
        
    # GET request: render the HTML form
    return render(request, 'residents/add_family_member.html')

@login_required
def add_vehicle_view(request):
    """
    Provides a form for residents to register a vehicle (Car/Bike).
    """
    if request.method == 'POST':
        number = request.POST.get('number')
        vehicle_type = request.POST.get('type')
        parking_slot = request.POST.get('parking_slot')
        
        # Link the new vehicle to the currently logged-in user's profile
        profile = get_object_or_404(ResidentProfile, user=request.user)
        services.add_vehicle(profile.id, number, vehicle_type, parking_slot)
        
        # Send them back to their dashboard once saved
        return redirect('resident_dashboard_data')
        
    # GET request: render the HTML form
    return render(request, 'residents/add_vehicle.html')


from django.shortcuts import get_object_or_404
from core.models import User
from .models import ResidentProfile, Flat, FamilyMember, Vehicle

# --- Resident Profile Management ---

def create_resident_profile(user_id, flat_id=None, move_in_date=None):
    """
    Creates a new ResidentProfile for an existing User.
    Optionally assigns them to a Flat and sets a move-in date.
    """
    user = get_object_or_404(User, id=user_id)
    flat = get_object_or_404(Flat, id=flat_id) if flat_id else None
    
    # get_or_create ensures we don't accidentally create duplicate profiles for the same user
    profile, created = ResidentProfile.objects.get_or_create(
        user=user,
        defaults={'flat': flat, 'move_in_date': move_in_date}
    )
    return profile, created

def assign_flat(resident_id, flat_id):
    """
    Links a ResidentProfile to a specific Flat.
    Typically used by the Admin during onboarding.
    """
    profile = get_object_or_404(ResidentProfile, id=resident_id)
    flat = get_object_or_404(Flat, id=flat_id)
    profile.flat = flat
    profile.save()
    return profile

def update_resident_info(resident_id, data):
    """
    Updates the fields on a ResidentProfile (e.g., move_in_date).
    """
    profile = get_object_or_404(ResidentProfile, id=resident_id)
    if 'move_in_date' in data:
        profile.move_in_date = data['move_in_date']
    profile.save()
    return profile

# --- Directory & Search ---

def list_residents(building_id=None, flat_id=None):
    """
    Returns a queryset of ResidentProfiles.
    Can be filtered by a specific building or flat.
    Uses select_related to optimize database queries for linked User and Flat data.
    """
    queryset = ResidentProfile.objects.select_related('user', 'flat__building')
    if building_id:
        queryset = queryset.filter(flat__building_id=building_id)
    if flat_id:
        queryset = queryset.filter(flat_id=flat_id)
    return queryset

def search_resident(query):
    """
    Searches for residents by matching their email address.
    icontains = case-insensitive partial match.
    """
    return ResidentProfile.objects.filter(user__email__icontains=query)

def get_resident_dashboard_data(user_id):
    """
    Aggregates all the necessary data for the Resident's personal dashboard.
    Fetches their profile, flat info, family members, registered vehicles, and outstanding dues.
    """
    from finance.models import Invoice
    from django.db.models import Sum
    profile = get_object_or_404(ResidentProfile, user_id=user_id)
    outstanding_dues = Invoice.objects.filter(resident=profile, status='unpaid').aggregate(Sum('amount'))['amount__sum'] or 0
    return {
        'resident': profile,
        'flat': profile.flat,
        'family_members': profile.family_members.all(),
        'vehicles': profile.vehicles.all(),
        'outstanding_dues': outstanding_dues
    }

# --- Family Member Management ---

def add_family_member(resident_id, name, relation, phone=None):
    """
    Creates a new FamilyMember linked to the given ResidentProfile.
    """
    profile = get_object_or_404(ResidentProfile, id=resident_id)
    return FamilyMember.objects.create(
        resident=profile,
        name=name,
        relation=relation,
        phone=phone
    )

def update_family_member(member_id, data):
    """
    Dynamically updates provided fields for an existing FamilyMember.
    """
    member = get_object_or_404(FamilyMember, id=member_id)
    for key, value in data.items():
        if hasattr(member, key):
            setattr(member, key, value)
    member.save()
    return member

def delete_family_member(member_id):
    """
    Removes a FamilyMember from the database.
    """
    member = get_object_or_404(FamilyMember, id=member_id)
    member.delete()
    return True

# --- Vehicle Management ---

def add_vehicle(resident_id, number, vehicle_type, parking_slot=None):
    """
    Registers a new Vehicle under a ResidentProfile.
    """
    profile = get_object_or_404(ResidentProfile, id=resident_id)
    return Vehicle.objects.create(
        resident=profile,
        number=number,
        type=vehicle_type,
        parking_slot=parking_slot
    )

def update_vehicle(vehicle_id, data):
    """
    Dynamically updates provided fields for an existing Vehicle.
    """
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    for key, value in data.items():
        if hasattr(vehicle, key):
            setattr(vehicle, key, value)
    vehicle.save()
    return vehicle

def list_vehicles(resident_id):
    """
    Returns all vehicles registered to a specific resident.
    """
    return Vehicle.objects.filter(resident_id=resident_id)

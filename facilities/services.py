from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Facility, FacilityBooking
from residents.models import ResidentProfile

def list_facilities():
    """
    Returns a queryset of all facilities available in the society.
    """
    return Facility.objects.all()

def check_availability(facility_id, date, start_time, end_time, exclude_booking_id=None):
    """
    Checks if there are any conflicting confirmed or pending bookings 
    for the requested facility, date, and time range.
    """
    conflicts = FacilityBooking.objects.filter(
        facility_id=facility_id,
        date=date,
        status__in=['pending', 'confirmed']
    ).filter(
        Q(start_time__lt=end_time) & Q(end_time__gt=start_time)
    )
    if exclude_booking_id:
        conflicts = conflicts.exclude(id=exclude_booking_id)
    return not conflicts.exists()

def book_facility(facility_id, date, start_time, end_time, resident_id=None, booked_by_user=None):
    """
    Creates a FacilityBooking. Either resident_id (for residents) or 
    booked_by_user (for admins) must be provided.
    """
    if not check_availability(facility_id, date, start_time, end_time):
        raise ValueError("The facility is already booked for this time slot.")
        
    facility = get_object_or_404(Facility, id=facility_id)
    
    kwargs = {
        'facility': facility,
        'date': date,
        'start_time': start_time,
        'end_time': end_time,
        'payment_status': 'paid' if facility.booking_fee == 0 else 'unpaid',
    }
    
    if resident_id:
        kwargs['resident'] = get_object_or_404(ResidentProfile, id=resident_id)
    if booked_by_user:
        kwargs['booked_by'] = booked_by_user
    
    return FacilityBooking.objects.create(**kwargs)

def cancel_booking(booking_id, user):
    """
    Cancels a booking if it belongs to the requesting user (resident or admin).
    """
    booking = get_object_or_404(FacilityBooking, id=booking_id)
    # Allow cancel if admin booked it, OR if it belongs to the resident's profile
    if booking.booked_by == user or (booking.resident and booking.resident.user == user):
        booking.status = 'cancelled'
        booking.save()
        return booking
    raise PermissionError("You are not allowed to cancel this booking.")

def get_resident_bookings(resident_id):
    """
    Returns a queryset of all bookings made by a specific resident, ordered by newest first.
    """
    return FacilityBooking.objects.filter(resident_id=resident_id).order_by('-date', '-start_time')

def get_admin_bookings(user):
    """
    Returns all bookings made by this admin user.
    """
    return FacilityBooking.objects.filter(booked_by=user).order_by('-date', '-start_time')


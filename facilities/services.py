from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Facility, FacilityBooking
from residents.models import ResidentProfile
import razorpay
from django.conf import settings

def _razorpay_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

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
    from datetime import date as date_obj, time as time_obj
    
    # Convert strings to objects if necessary
    if isinstance(date, str):
        date = date_obj.fromisoformat(date)
    if isinstance(start_time, str):
        start_time = time_obj.fromisoformat(start_time)
    if isinstance(end_time, str):
        end_time = time_obj.fromisoformat(end_time)

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
        
    from datetime import date as date_obj, time as time_obj
    if isinstance(date, str):
        date = date_obj.fromisoformat(date)
    if isinstance(start_time, str):
        start_time = time_obj.fromisoformat(start_time)
    if isinstance(end_time, str):
        end_time = time_obj.fromisoformat(end_time)

    facility = get_object_or_404(Facility, id=facility_id)
    
    kwargs = {
        'facility': facility,
        'date': date,
        'start_time': start_time,
        'end_time': end_time,
        'payment_status': 'paid' if facility.fee == 0 else 'unpaid',
    }
    
    if resident_id:
        kwargs['resident'] = get_object_or_404(ResidentProfile, id=resident_id)
    if booked_by_user:
        kwargs['booked_by'] = booked_by_user
        kwargs['status'] = 'confirmed' # Admin bookings are auto-confirmed
        kwargs['payment_status'] = 'paid'
    elif facility.fee == 0:
        kwargs['status'] = 'confirmed' # Free resident bookings auto-confirmed
    else:
        kwargs['status'] = 'pending' # Paid resident bookings need approval
        
    return FacilityBooking.objects.create(**kwargs)

def approve_booking(booking_id):
    """
    Admin function to confirm a resident's facility reservation.
    """
    booking = get_object_or_404(FacilityBooking, id=booking_id)
    if booking.status == 'pending':
        booking.status = 'confirmed'
        booking.save()
        return True
    return False

def reject_booking(booking_id):
    """
    Admin function to decline a facility reservation.
    """
    booking = get_object_or_404(FacilityBooking, id=booking_id)
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        return True
    return False

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

def edit_booking(booking_id, user, facility_id, date, start_time, end_time):
    """
    Edits an existing booking if the user has permission to do so.
    """
    booking = get_object_or_404(FacilityBooking, id=booking_id)
    
    # Permission check: must be admin who booked it, or resident who owns it
    is_owner = (booking.booked_by == user) or (booking.resident and booking.resident.user == user)
    is_admin = user.role == 'admin'
    
    if not (is_owner or is_admin):
        raise PermissionError("You do not have permission to edit this booking.")
        
    if not check_availability(facility_id, date, start_time, end_time, exclude_booking_id=booking_id):
        raise ValueError("The facility is already booked for this new time slot.")
        
    facility = get_object_or_404(Facility, id=facility_id)
    
    booking.facility = facility
    booking.date = date
    booking.start_time = start_time
    booking.end_time = end_time
    booking.save()
    return booking

def create_booking_razorpay_order(amount_inr):
    """
    Creates a Razorpay order for facility booking.
    """
    client = _razorpay_client()
    amount_paise = int(float(amount_inr) * 100)
    order = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'payment_capture': 1,
    })
    return order

def verify_booking_payment_signature(payment_id, order_id, signature):
    """
    Verifies Razorpay signature for facility booking.
    """
    client = _razorpay_client()
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
        })
        return True
    except razorpay.errors.SignatureVerificationError:
        return False


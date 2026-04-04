from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from . import services
from .models import FacilityBooking, Facility
from residents.models import ResidentProfile

@login_required
def facility_list_view(request):
    """
    Shows all available society amenities. Role-aware: Admins get admin layout.
    """
    facilities = services.list_facilities()
    if request.user.role == 'admin':
        base_template = 'admin_base.html'
    elif request.user.role == 'security':
        base_template = 'security_base.html'
    else:
        base_template = 'resident_base.html'
    return render(request, 'facilities/list.html', {
        'facilities': facilities,
        'base_template': base_template,
        'is_admin': request.user.role == 'admin',
    })

@login_required
def book_facility_view(request):
    """
    View to book a timeslot for a facility. Works for both residents and admins.
    """
    if request.user.role not in ('resident', 'admin'):
        return redirect('security_dashboard')
        
    if request.method == 'POST':
        facility_id = request.POST.get('facility_id')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        try:
            if request.user.role == 'admin':
                booking = services.book_facility(
                    facility_id=facility_id,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    booked_by_user=request.user,
                )
                # Admins go to their own bookings list after booking
                return redirect('my_bookings')
            else:
                profile = ResidentProfile.objects.get(user=request.user)
                booking = services.book_facility(
                    facility_id=facility_id,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    resident_id=profile.id,
                )
                if booking.payment_status == 'unpaid':
                    return redirect('pay_booking', booking_id=booking.id)
                return redirect('my_bookings')
        except ValueError as e:
            facilities = services.list_facilities()
            return render(request, 'facilities/book.html', {'error': str(e), 'facilities': facilities})
        except ResidentProfile.DoesNotExist:
            return redirect('resident_dashboard')
    
    # Determine the base template for role-aware rendering
    base_template = 'admin_base.html' if request.user.role == 'admin' else 'resident_base.html'
    return render(request, 'facilities/book.html', {
        'facilities': services.list_facilities(),
        'base_template': base_template,
    })

@login_required
def edit_booking_view(request, booking_id):
    """
    View to edit an existing facility booking timeslot.
    Reuses the book.html template with pre-filled context.
    """
    booking = get_object_or_404(FacilityBooking, id=booking_id)
    
    # Simple permission verification
    is_owner = (booking.booked_by == request.user) or (booking.resident and booking.resident.user == request.user)
    is_admin = request.user.role == 'admin'
    if not (is_owner or is_admin):
        return redirect('my_bookings')
        
    facilities = services.list_facilities()
    
    if request.method == 'POST':
        facility_id = request.POST.get('facility_id')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        try:
            services.edit_booking(
                booking_id=booking.id,
                user=request.user,
                facility_id=facility_id,
                date=date,
                start_time=start_time,
                end_time=end_time
            )
            return redirect('my_bookings')
        except (ValueError, PermissionError) as e:
            base_template = 'admin_base.html' if request.user.role == 'admin' else 'resident_base.html'
            return render(request, 'facilities/book.html', {
                'facilities': facilities, 
                'base_template': base_template,
                'booking': booking,
                'error': str(e)
            })

    base_template = 'admin_base.html' if request.user.role == 'admin' else 'resident_base.html'
    return render(request, 'facilities/book.html', {
        'facilities': facilities,
        'base_template': base_template,
        'booking': booking,
    })

@login_required
def my_bookings_view(request):
    """
    View listing bookings for the current user (resident or admin).
    """
    if request.user.role == 'admin':
        bookings = services.get_admin_bookings(request.user)
        return render(request, 'facilities/my_bookings.html', {
            'bookings': bookings,
            'base_template': 'admin_base.html',
        })
    elif request.user.role == 'resident':
        try:
            profile = ResidentProfile.objects.get(user=request.user)
            bookings = services.get_resident_bookings(profile.id)
        except ResidentProfile.DoesNotExist:
            bookings = []
        return render(request, 'facilities/my_bookings.html', {
            'bookings': bookings,
            'base_template': 'resident_base.html',
        })
    return redirect('security_dashboard')

@login_required
def api_facility_bookings(request, facility_id):
    """
    Returns JSON of confirmed/pending bookings for FullCalendar integration.
    """
    facility = get_object_or_404(Facility, id=facility_id)
    bookings = FacilityBooking.objects.filter(
        facility=facility,
        status__in=['pending', 'confirmed']
    )
    
    events = []
    for b in bookings:
        start_dt = f"{b.date.isoformat()}T{b.start_time.strftime('%H:%M:00')}"
        end_dt = f"{b.date.isoformat()}T{b.end_time.strftime('%H:%M:00')}"
        events.append({
            'title': 'Booked',
            'start': start_dt,
            'end': end_dt,
            'color': '#10B981' if b.status == 'confirmed' else '#F59E0B'
        })
    return JsonResponse(events, safe=False)

@login_required
def pay_booking_view(request, booking_id):
    """
    Resident view to pay for a facility booking.
    """
    if request.user.role != 'resident':
        return redirect('admin_dashboard')
        
    try:
        profile = ResidentProfile.objects.get(user=request.user)
        booking = FacilityBooking.objects.get(id=booking_id, resident=profile, payment_status='unpaid')
    except (ResidentProfile.DoesNotExist, FacilityBooking.DoesNotExist):
        return redirect('my_bookings')
        
    if request.method == 'POST':
        # Simulate payment processing (in reality, verify against a gateway)
        transaction_id = request.POST.get('transaction_id')
        if transaction_id:
            booking.payment_status = 'paid'
            booking.save()
            return redirect('my_bookings')
            
    return render(request, 'facilities/pay_booking.html', {'booking': booking})


@login_required
def cancel_booking_view(request, booking_id):
    """
    Cancels a facility booking. Works for both residents and admins
    if they own the booking.
    """
    if request.method == 'POST':
        try:
            services.cancel_booking(booking_id, request.user)
        except PermissionError:
            pass  # Silently ignore unauthorized attempts
    return redirect('my_bookings')


@login_required
def approve_booking_view(request, booking_id):
    """
    Endpoint for admins to confirm a resident's amenity booking.
    """
    if request.user.role != 'admin':
        return redirect('admin_dashboard')
    
    from django.contrib import messages
    if services.approve_booking(booking_id):
        messages.success(request, f"Booking #{booking_id} has been confirmed.")
    else:
        messages.error(request, "Failed to confirm. Booking might not be in pending state.")
    
    return redirect('admin_dashboard')

@login_required
def reject_booking_view(request, booking_id):
    """
    Endpoint for admins to decline an amenity booking.
    """
    if request.user.role != 'admin':
        return redirect('admin_dashboard')
    
    from django.contrib import messages
    if services.reject_booking(booking_id):
        messages.warning(request, f"Booking #{booking_id} has been cancelled.")
    else:
        messages.error(request, "Failed to cancel. Booking might not be in pending state.")
    
    return redirect('admin_dashboard')


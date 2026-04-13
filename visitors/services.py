from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Visitor
from residents.models import ResidentProfile

# --- Visitor Management Services ---

def create_visitor_request(resident_id, visitor_data):
    """
    Creates a new visitor log. Automatically sets status to 'pending'.
    """
    profile = get_object_or_404(ResidentProfile, id=resident_id)
    return Visitor.objects.create(
        resident=profile,
        name=visitor_data.get('name'),
        phone=visitor_data.get('phone'),
        purpose=visitor_data.get('purpose'),
        vehicle_number=visitor_data.get('vehicle_number', ''),
        visit_date=visitor_data.get('visit_date'),
        visit_time=visitor_data.get('visit_time'),
        description=visitor_data.get('description', '')
    )

def update_visitor_status(visitor_id, new_status):
    """
    Updates the physical status of a visitor.
    If they are marked as 'exited', their exit time is recorded automatically.
    """
    visitor = get_object_or_404(Visitor, id=visitor_id)
    visitor.status = new_status
    
    # Automatically log the time they exited the premises
    if new_status == 'exited' and not visitor.exit_time:
        visitor.exit_time = timezone.now()
        
    visitor.save()
    return visitor

def get_expected_visitors():
    """
    Fetches all visitors who are pending or approved but haven't entered yet.
    Useful for the security guard dashboard.
    """
    return Visitor.objects.filter(status__in=['pending', 'approved']).order_by('-entry_time')

def get_resident_visitors(resident_id):
    """
    Fetches all visitor logs for a specific resident.
    """
    return Visitor.objects.filter(resident_id=resident_id).order_by('-entry_time')

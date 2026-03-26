from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Complaint
from residents.models import ResidentProfile

# --- Complaint Management Services ---

def create_complaint(resident_id, data):
    """
    Raises a new complaint and assigns it 'open' status by default.
    """
    profile = get_object_or_404(ResidentProfile, id=resident_id)
    return Complaint.objects.create(
        resident=profile,
        category=data.get('category'),
        title=data.get('title'),
        description=data.get('description')
    )

def update_complaint_status(complaint_id, new_status, remarks=None):
    """
    Allows Admin or Facilities to update the status of a complaint and leave remarks.
    Automatically updates the 'updated_at' timestamp.
    """
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.status = new_status
    if remarks:
        complaint.resolution_remarks = remarks
    complaint.updated_at = timezone.now()
    complaint.save()
    return complaint

def get_resident_complaints(resident_id):
    """
    Returns a resident's complaint history logic.
    """
    return Complaint.objects.filter(resident_id=resident_id).order_by('-created_at')

def get_all_complaints(status=None):
    """
    Fetch all complaints. Admin can optionally filter them by open/closed status.
    """
    queryset = Complaint.objects.select_related('resident__user', 'resident__flat__building')
    if status:
        queryset = queryset.filter(status=status)
    return queryset.order_by('-created_at')

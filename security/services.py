from django.shortcuts import get_object_or_404
from .models import EmergencyAlert
from residents.models import ResidentProfile

def raise_emergency(resident_id, alert_type, description=""):
    """
    Creates a new high-priority active alert linked to a resident.
    It defaults to 'active' status so that security guards see it immediately.
    """
    profile = get_object_or_404(ResidentProfile, id=resident_id)
    return EmergencyAlert.objects.create(
        resident=profile,
        alert_type=alert_type,
        description=description
    )

def get_active_emergencies():
    """
    Pulls all unresolved emergencies, sorted by newest first.
    Used to populate the real-time security guard dashboard.
    """
    return EmergencyAlert.objects.filter(status='active').order_by('-timestamp')

def resolve_emergency(alert_id):
    """
    Marks an emergency alert as handled/resolved after security investigates.
    """
    alert = get_object_or_404(EmergencyAlert, id=alert_id)
    alert.status = 'resolved'
    alert.save()
    return alert

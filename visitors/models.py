from django.db import models
from residents.models import ResidentProfile

class Visitor(models.Model):
    """
    Tracks individuals visiting a specific resident in the society.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('entered', 'Entered Society'),
        ('exited', 'Exited Society'),
    )

    # The resident the visitor is coming to see
    resident = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='visitors')
    
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    purpose = models.CharField(max_length=255) # e.g., "Guest", "Delivery", "Maintenance"
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Tracking the timeline
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.name} visiting {self.resident.user.email} ({self.get_status_display()})"

from django.db import models
from residents.models import ResidentProfile

class Complaint(models.Model):
    """
    Tracks maintenance or administrative issues raised by a resident.
    """
    CATEGORY_CHOICES = (
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('security', 'Security'),
        ('noise', 'Noise Disturbance'),
        ('other', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )

    resident = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='complaints')
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    # Optional field for the admin/maintenance team to explain the fix
    resolution_remarks = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.resident.user.email} ({self.get_status_display()})"

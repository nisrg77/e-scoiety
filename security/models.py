from django.db import models
from residents.models import ResidentProfile

class EmergencyAlert(models.Model):
    """
    High-priority alerts triggered by residents for the security team.
    These bypass normal complaints and immediately notify the dashboard.
    """
    ALERT_TYPES = (
        ('fire', 'Fire Alarm'),
        ('medical', 'Medical Emergency'),
        ('security', 'Security Breach'),
        ('other', 'Other'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('resolved', 'Resolved'),
    )
    
    # The resident who pressed the panic button
    resident = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    description = models.TextField(blank=True) # Optional context
    
    timestamp = models.DateTimeField(auto_now_add=True) # Exact time the alert was raised
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.get_alert_type_display()} by {self.resident.user.email} - {self.get_status_display()}"

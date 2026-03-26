from django.db import models
from django.conf import settings
from residents.models import ResidentProfile

class Facility(models.Model):
    """
    Shared amenities available in the society.
    """
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(default=1)
    booking_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class FacilityBooking(models.Model):
    """
    Tracks a resident's reservation of a specific facility.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    )

    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='bookings')
    resident = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='facility_bookings', null=True, blank=True)
    booked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_bookings')
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='unpaid')
    
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def booker_label(self):
        if self.resident:
            return self.resident.user.email
        elif self.booked_by:
            return f"{self.booked_by.get_full_name() or self.booked_by.email} (Admin)"
        return "Unknown"

    def __str__(self):
        return f"{self.facility.name} booked by {self.booker_label} on {self.date}"

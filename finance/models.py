from django.db import models
from residents.models import ResidentProfile

class Invoice(models.Model):
    """
    Represents a monthly maintenance bill or special charge for a resident.
    """
    STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    )
    resident = models.ForeignKey(ResidentProfile, on_delete=models.CASCADE, related_name='invoices')
    month = models.PositiveIntegerField() # e.g. 5 for May
    year = models.PositiveIntegerField() # e.g. 2026
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255) # "Monthly Maintenance"
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id} for {self.resident.user.email} - {self.get_status_display()}"


class Payment(models.Model):
    """
    Tracks a transaction paying off an invoice.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return f"Payment of {self.amount_paid} for Invoice #{self.invoice.id}"


class SocietyExpense(models.Model):
    """
    Tracks outgoing funds spent by the society administration.
    """
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=100) # Maintenance, Salary, Utilities, etc.

    def __str__(self):
        return f"{self.title} - {self.amount}"

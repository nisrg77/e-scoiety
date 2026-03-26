from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .models import Invoice, Payment, SocietyExpense
from residents.models import ResidentProfile

def generate_monthly_invoices(year, month, amount, due_date, description="Monthly Maintenance"):
    """
    Admin function to bulk generate invoices for all residents currently occupying flats.
    Returns a list of newly created invoices.
    """
    # Only bill residents who have been assigned to flats (flat is not null)
    residents = ResidentProfile.objects.exclude(flat__isnull=True)
    invoices = []
    
    for resident in residents:
        # get_or_create ensures we don't accidentally double-bill a resident for the same month/year
        inv, created = Invoice.objects.get_or_create(
            resident=resident,
            month=month,
            year=year,
            defaults={
                'amount': amount,
                'description': description,
                'due_date': due_date
            }
        )
        if created:
            invoices.append(inv)
            
    return invoices

def get_resident_invoices(resident_id):
    """
    Fetches the billing history (both paid and unpaid invoices) for a specific resident.
    """
    return Invoice.objects.filter(resident_id=resident_id).order_by('-year', '-month')

def record_payment(invoice_id, amount, transaction_id=None):
    """
    Logs a Payment transaction against an Invoice. 
    If the cumulative payments equal or exceed the total invoice amount,
    it automatically updates the Invoice status from 'unpaid' to 'paid'.
    """
    invoice = get_object_or_404(Invoice, id=invoice_id)
    payment = Payment.objects.create(
        invoice=invoice,
        amount_paid=amount,
        transaction_id=transaction_id
    )
    
    # Check if invoice is fully paid off.
    # We use Django's aggregate() function to calculate the sum directly in the SQL database,
    # rather than loading all payments into Python memory and summing them manually.
    total_paid = invoice.payments.aggregate(total=Sum('amount_paid'))['total'] or 0
    
    if total_paid >= invoice.amount:
        invoice.status = 'paid'
        invoice.save()
        
    return payment

def get_expense_report(start_date=None, end_date=None):
    """
    Admin function to fetch all outgoing society expenses.
    Can optionally be filtered by a start_date and end_date range constraint.
    """
    expenses = SocietyExpense.objects.all()
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    if end_date:
        expenses = expenses.filter(date__lte=end_date)
    return expenses.order_by('-date')

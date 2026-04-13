from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.conf import settings
from .models import Invoice, Payment, SocietyExpense
from residents.models import ResidentProfile
import razorpay

# ---------------------------------------------------------------------------
# Razorpay client (lazy init so missing keys don't crash on import)
# ---------------------------------------------------------------------------
def _razorpay_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


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

def create_razorpay_order(amount_inr):
    """
    Creates a Razorpay order for the given amount (in INR).
    Razorpay requires the amount in paise (1 INR = 100 paise).
    Returns the full order dict from Razorpay.
    """
    client = _razorpay_client()
    amount_paise = int(float(amount_inr) * 100)
    order = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'payment_capture': 1,  # Auto-capture on payment success
    })
    return order


def verify_razorpay_signature(payment_id, order_id, signature):
    """
    Verifies the HMAC-SHA256 signature from Razorpay to ensure
    the payment callback was not tampered with.
    Returns True if valid, False otherwise.
    """
    client = _razorpay_client()
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
        })
        return True
    except razorpay.errors.SignatureVerificationError:
        return False


def record_payment(invoice_id, amount, transaction_id=None, razorpay_order_id=None):
    """
    Logs a Payment transaction against an Invoice. 
    If the cumulative payments equal or exceed the total invoice amount,
    it automatically updates the Invoice status from 'unpaid' to 'pending' (awaiting admin approval).
    """
    invoice = get_object_or_404(Invoice, id=invoice_id)
    payment = Payment.objects.create(
        invoice=invoice,
        amount_paid=amount,
        transaction_id=transaction_id,
        razorpay_order_id=razorpay_order_id,
    )
    
    # Check if invoice is fully paid off.
    total_paid = invoice.payments.aggregate(total=Sum('amount_paid'))['total'] or 0
    
    if total_paid >= invoice.amount:
        invoice.status = 'pending'  # Set to pending for admin approval
        invoice.save()
        
    return payment

def approve_invoice(invoice_id):
    """
    Admin function to manually confirm a payment and mark an invoice as fully 'paid'.
    """
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if invoice.status == 'pending':
        invoice.status = 'paid'
        invoice.save()
        return True
    return False

def reject_invoice(invoice_id):
    """
    Admin function to reject a payment if the details are incorrect.
    """
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if invoice.status == 'pending':
        invoice.status = 'unpaid'
        invoice.save()
        return True
    return False

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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import services
from residents.models import ResidentProfile

@login_required
def my_invoices_view(request):
    """
    Resident dashboard to see their maintenance bills and outstanding dues.
    """
    if request.user.role != 'resident':
        return redirect('admin_dashboard')
        
    try:
        profile = ResidentProfile.objects.get(user=request.user)
        invoices = services.get_resident_invoices(profile.id)
    except ResidentProfile.DoesNotExist:
        invoices = []
        
    return render(request, 'finance/my_invoices.html', {'invoices': invoices})

@login_required
def pay_invoice_view(request, invoice_id):
    """
    Creates a Razorpay order and renders the payment page.
    The Razorpay checkout popup is opened automatically via JS.
    """
    if request.user.role != 'resident':
        return redirect('admin_dashboard')

    from .models import Invoice
    from django.conf import settings

    invoice = Invoice.objects.get(id=invoice_id)

    # Don't allow payment on already paid/pending invoices
    if invoice.status != 'unpaid':
        return redirect('my_invoices')

    # Create a Razorpay order
    order = services.create_razorpay_order(invoice.amount)

    context = {
        'invoice': invoice,
        'razorpay_order_id': order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount_paise': order['amount'],  # Already in paise
        'amount_inr': invoice.amount,
        'user_name': getattr(request.user, 'first_name', '') + ' ' + getattr(request.user, 'last_name', '') if hasattr(request.user, 'first_name') else request.user.email,
        'user_email': request.user.email,
    }
    return render(request, 'finance/pay_invoice.html', context)


@login_required
def verify_payment_view(request):
    """
    Handles the Razorpay payment callback.
    Verifies the HMAC signature and records the payment if valid.
    """
    if request.user.role != 'resident':
        return redirect('admin_dashboard')

    if request.method != 'POST':
        return redirect('my_invoices')

    from django.contrib import messages

    payment_id  = request.POST.get('razorpay_payment_id', '')
    order_id    = request.POST.get('razorpay_order_id', '')
    signature   = request.POST.get('razorpay_signature', '')
    invoice_id  = request.POST.get('invoice_id', '')

    # Verify the HMAC signature to prevent tampering
    if services.verify_razorpay_signature(payment_id, order_id, signature):
        invoice = Invoice.objects.get(id=invoice_id)
        services.record_payment(
            invoice_id=invoice_id,
            amount=invoice.amount,
            transaction_id=payment_id,
            razorpay_order_id=order_id,
        )
        messages.success(request, f"✅ Payment of ₹{invoice.amount} received! Pending admin verification.")
    else:
        messages.error(request, "❌ Payment verification failed. Please contact support.")

    return redirect('my_invoices')

@login_required
def expense_report_view(request):
    """
    Admin-only dashboard tool to view and record society expenditure.
    """
    if request.user.role != 'admin':
        return redirect('resident_dashboard')
    
    if request.method == 'POST':
        from .models import SocietyExpense
        from datetime import date
        title = request.POST.get('title', '').strip()
        amount = request.POST.get('amount', '').strip()
        category = request.POST.get('category', '').strip()
        expense_date = request.POST.get('date', '').strip() or date.today().isoformat()
        if title and amount:
            SocietyExpense.objects.create(
                title=title,
                amount=amount,
                category=category or 'General',
                date=expense_date,
            )
        return redirect('expense_report')
        
    expenses = services.get_expense_report()
    return render(request, 'finance/expense_report.html', {'expenses': expenses})

@login_required
def create_invoice_view(request):
    """
    Admin dashboard tool to generate maintenance dues for residents.
    """
    if request.user.role != 'admin':
        return redirect('resident_dashboard')
        
    residents = ResidentProfile.objects.all()
    
    if request.method == 'POST':
        from .models import Invoice
        from datetime import date
        
        resident_id = request.POST.get('resident_id')
        amount = request.POST.get('amount')
        description = request.POST.get('description', 'Monthly Maintenance')
        due_date = request.POST.get('due_date')
        
        # Determine month/year from due_date or today
        target_date = date.fromisoformat(due_date) if due_date else date.today()
        
        if resident_id == 'all':
            # Create for all assigned residents
            for res in residents:
                if res.flat: # Only for residents assigned to a flat
                    Invoice.objects.create(
                        resident=res,
                        amount=amount,
                        description=description,
                        month=target_date.month,
                        year=target_date.year,
                        due_date=target_date
                    )
        else:
            # Create for specific resident
            res = ResidentProfile.objects.get(id=resident_id)
            Invoice.objects.create(
                resident=res,
                amount=amount,
                description=description,
                month=target_date.month,
                year=target_date.year,
                due_date=target_date
            )
            
        return redirect('expense_report') # Redirecting to finance hub
        
    return render(request, 'finance/create_invoice.html', {'residents': residents})

@login_required
def approve_payment_view(request, invoice_id):
    """
    Endpoint for admins to confirm a resident's payment.
    """
    if request.user.role != 'admin':
        return redirect('admin_dashboard')
    
    from . import services
    from django.contrib import messages
    if services.approve_invoice(invoice_id):
        messages.success(request, f"Invoice #{invoice_id} has been approved and marked as Paid.")
    else:
        messages.error(request, "Failed to approve. Invoice might not be in pending state.")
    
    return redirect('admin_dashboard')

@login_required
def reject_payment_view(request, invoice_id):
    """
    Endpoint for admins to decline a suspicious or incorrect payment.
    """
    if request.user.role != 'admin':
        return redirect('admin_dashboard')
    
    from . import services
    from django.contrib import messages
    if services.reject_invoice(invoice_id):
        messages.warning(request, f"Payment for Invoice #{invoice_id} has been rejected.")
    else:
        messages.error(request, "Failed to reject. Invoice might not be in pending state.")
    
    return redirect('admin_dashboard')

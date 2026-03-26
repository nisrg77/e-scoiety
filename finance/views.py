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
    Mock payment processing endpoint for a specific invoice.
    """
    if request.user.role != 'resident':
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        amount = request.POST.get('amount')
        transaction_id = request.POST.get('transaction_id')
        services.record_payment(invoice_id, amount, transaction_id)
        return redirect('my_invoices')
        
    return render(request, 'finance/pay_invoice.html', {'invoice_id': invoice_id})
    
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

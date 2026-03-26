from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import services
from residents.models import ResidentProfile

@login_required
def raise_complaint_view(request):
    """
    Resident view to submit a new complaint.
    """
    if request.user.role != 'resident':
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        data = {
            'category': request.POST.get('category'),
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
        }
        
        profile = get_object_or_404(ResidentProfile, user=request.user)
        services.create_complaint(profile.id, data)
        return redirect('my_complaints')
        
    return render(request, 'complaints/raise_complaint.html')

@login_required
def my_complaints_view(request):
    """
    Resident view to list all complaints they have previously raised.
    """
    if request.user.role != 'resident':
        return redirect('admin_dashboard')
        
    profile = get_object_or_404(ResidentProfile, user=request.user)
    complaints = services.get_resident_complaints(profile.id)
    return render(request, 'complaints/my_complaints.html', {'complaints': complaints})

@login_required
def manage_complaints_view(request):
    """
    Admin view to see all society complaints and update their status.
    """
    if request.user.role != 'admin':
        return redirect('resident_dashboard')
        
    # Handle POST request to update a complaint's status
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        new_status = request.POST.get('status')
        remarks = request.POST.get('remarks')
        
        services.update_complaint_status(complaint_id, new_status, remarks)
        return redirect('manage_complaints')

    # GET request: fetch all complaints, optionally filtered by status
    status_filter = request.GET.get('status')
    complaints = services.get_all_complaints(status_filter)
    return render(request, 'complaints/manage_complaints.html', {'complaints': complaints})

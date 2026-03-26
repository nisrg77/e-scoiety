from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import services
from residents.models import ResidentProfile

@login_required
def add_visitor_view(request):
    """
    Resident view to pre-approve or log a visitor to their flat.
    """
    if request.user.role != 'resident':
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'purpose': request.POST.get('purpose'),
            'vehicle_number': request.POST.get('vehicle_number'),
        }
        
        profile = ResidentProfile.objects.filter(user=request.user).first()
        if profile:
            services.create_visitor_request(profile.id, data)
        return redirect('my_visitors')
        
    return render(request, 'visitors/add_visitor.html')

@login_required
def my_visitors_view(request):
    """
    Resident view to see their visitor log.
    """
    if request.user.role != 'resident':
        return redirect('admin_dashboard')
        
    profile = ResidentProfile.objects.filter(user=request.user).first()
    if not profile:
        return render(request, 'visitors/my_visitors.html', {'visitors': []})
        
    visitors = services.get_resident_visitors(profile.id)
    return render(request, 'visitors/my_visitors.html', {'visitors': visitors})

@login_required
def security_visitor_log_view(request):
    """
    Security view to track expected visitors and mark entry/exit.
    """
    if request.user.role != 'security':
        return redirect('resident_dashboard')
        
    if request.method == 'POST':
        visitor_id = request.POST.get('visitor_id')
        new_status = request.POST.get('status')
        services.update_visitor_status(visitor_id, new_status)
        return redirect('security_visitor_log')

    expected_visitors = services.get_expected_visitors()
    return render(request, 'visitors/security_log.html', {'visitors': expected_visitors})

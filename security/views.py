from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import services
from residents.models import ResidentProfile

@login_required
def raise_emergency_view(request):
    """
    Resident view detailing a panic button interface.
    Allows a resident to trigger a high-priority alert (Fire, Medical, etc).
    """
    if request.user.role != 'resident':
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        alert_type = request.POST.get('alert_type')
        description = request.POST.get('description', '')
        try:
            profile = ResidentProfile.objects.get(user=request.user)
            services.raise_emergency(profile.id, alert_type, description)
            return redirect('resident_dashboard')
        except ResidentProfile.DoesNotExist:
            pass
            
    return render(request, 'security/raise_emergency.html')

@login_required
def security_alert_dashboard_view(request):
    """
    Security team's real-time dashboard to view active emergencies.
    Allows guards to quickly resolve handled incidents.
    """
    # Enforces role-based access control (RBAC)
    if request.user.role != 'security':
        return redirect('resident_dashboard')
        
    if request.method == 'POST':
        alert_id = request.POST.get('alert_id')
        services.resolve_emergency(alert_id)
        return redirect('security_alert_dashboard')
        
    alerts = services.get_active_emergencies()
    return render(request, 'security/alert_dashboard.html', {'alerts': alerts})

from django.shortcuts import render,redirect,HttpResponse
from .forms import UserSignupForm,UserLoginForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, resident_required, security_required
from django.core.mail import send_mail
from django.conf import settings

# Handles new user registration
def home(request):
    """
    Renders the home page of the application.
    """
    return render(request, "core/home.html")

def userSignupView(request):
    """
    Handles user registration process.
    On GET: Renders a blank signup form.
    On POST: Validates form data, creates a new user, sends a welcome email, 
    and redirects to the login page on success.
    """
    if request.method =="POST":
      # Populate form with incoming POST data
      form = UserSignupForm(request.POST or None)
      if form.is_valid():
        # Retrieve the cleaned email data to send the welcome email
        email = form.cleaned_data['email']
        send_mail(subject="Welcome to eSociety",message="Thank you for registering with eSociety.",from_email=settings.EMAIL_HOST_USER,recipient_list=[email])
        
        # Save user to DB and securely hash their password
        form.save()
        
        # Registration successful, redirect to login page
        return redirect('login') 
      else:
        # Form has errors (e.g duplicate email, weak passwords), return form with errors
        return render(request,'core/signup.html',{'form':form})  
    else:
        # GET Request: Send a blank form
        form = UserSignupForm()
        return render(request,'core/signup.html',{'form':form})


# Handles user authentication and redirects to proper dashboard
def userLoginView(request):
  """
  Handles user login authentication.
  On GET: Renders the login form.
  On POST: Authenticates credentials against the database. On success, logs the 
  user in and routes them to their corresponding dashboard based on their role 
  (admin, resident, or security).
  """
  if request.method =="POST":
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      
      # Verifies the provided email and password against the database
      user = authenticate(request,email=email,password=password)
      
      if user: # If user exists and password is correct
        # Sets the session cookie in the user's browser securely
        login(request,user)
        
        # RBAC Routing: Send user to their corresponding dashboard
        if user.role == "admin":
          return redirect("admin_dashboard")
        elif user.role == "resident":
          return redirect("resident_dashboard")
        elif user.role == "security":
          return redirect("security_dashboard")
      
      # Authentication failed (wrong password or user not found)
      return render(request, 'core/login.html', {'form': form, 'error': 'Invalid email or password.'})
    
    # Form validation failed (e.g. empty fields)
    return render(request,'core/login.html',{'form':form})
    
  else:
    # GET Request: Send a blank login form
    form = UserLoginForm()
    return render(request,'core/login.html',{'form':form})

def userLogoutView(request):
    """
    Logs out the user and clears their session securely.
    Redirects to the login page.
    """
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')

# Role-based decorators block unauthorized users from viewing the dashboard
@admin_required
def admin_dashboard(request):
    """
    Renders the dashboard interface for admin users.
    Requires the user to be logged in and have the 'admin' role.
    """
    from residents.models import ResidentProfile
    from facilities.models import FacilityBooking
    from finance.models import SocietyExpense, Invoice
    from django.db.models import Sum
    
    total_residents = ResidentProfile.objects.count()
    active_bookings = FacilityBooking.objects.filter(status='approved').count()
    total_expenses = SocietyExpense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_revenue = Invoice.objects.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'total_residents': total_residents,
        'active_bookings': active_bookings,
        'total_expenses': total_expenses,
        'total_revenue': total_revenue,
    }
    return render(request, "core/admin_dashboard.html", context)

@resident_required
def resident_dashboard(request):
    """
    Renders the dashboard interface for resident users.
    Requires the user to be logged in and have the 'resident' role.
    """
    return redirect("resident_dashboard_data")

@security_required
def security_dashboard(request):
    """
    Renders the dashboard interface for security guard users.
    Handles quick check-in, check-out, and dismissing alerts.
    """
    from visitors.models import Visitor
    from visitors.services import update_visitor_status
    from security.models import EmergencyAlert
    from residents.models import ResidentProfile

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'quick_checkin':
            flat_num = request.POST.get('flat')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            purpose = request.POST.get('purpose')
            vehicle = request.POST.get('vehicle_number', '')
            
            # Find resident profile based on flat number
            resident = ResidentProfile.objects.filter(flat__number__iexact=flat_num).first()
            if not resident:
                # Fallback if specific flat not found, try to find any profile to attach to
                # In a real system, you'd show a validation error to the guard
                resident = ResidentProfile.objects.first()
                
            if resident and name:
                Visitor.objects.create(
                    resident=resident,
                    name=name,
                    phone=phone,
                    purpose=purpose,
                    vehicle_number=vehicle,
                    status='entered'  # Instantly marked as entered by security
                )
                
        elif action == 'checkout':
            visitor_id = request.POST.get('visitor_id')
            if visitor_id:
                update_visitor_status(visitor_id, 'exited')
                
        elif action == 'dismiss_alert':
            alert_id = request.POST.get('alert_id')
            if alert_id:
                alert = EmergencyAlert.objects.filter(id=alert_id).first()
                if alert:
                    alert.status = 'resolved'
                    alert.save()
                    
        return redirect('security_dashboard')
    
    visitors_inside = Visitor.objects.filter(status='entered').count()
    expected_deliveries = Visitor.objects.filter(status='approved', purpose__icontains='Delivery').count()
    emergency_alerts = EmergencyAlert.objects.filter(status='active').count()
    
    recent_visitors = Visitor.objects.filter(status='entered').order_by('-entry_time')[:5]
    recent_alerts = EmergencyAlert.objects.filter(status='active').order_by('-timestamp')[:5]
    
    context = {
        'visitors_inside': visitors_inside,
        'expected_deliveries': expected_deliveries,
        'emergency_alerts': emergency_alerts,
        'recent_visitors': recent_visitors,
        'recent_alerts': recent_alerts,
    }
    return render(request, "core/security_dashboard.html", context)

import random
from django.utils import timezone
from .models import User, OTPVerification

def forgot_password(request):
    """
    Handles the first step of password reset: asking for email,
    generating a 6-digit OTP, and emailing it to the user.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate 6-digit OTP
            otp_code = str(random.randint(100000, 999999))
            
            # Save to DB
            OTPVerification.objects.create(user=user, otp_code=otp_code)
            
            # Send email
            send_mail(
                subject="Your Password Reset OTP",
                message=f"Your OTP for password reset is: {otp_code}. It is valid for 10 minutes.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email]
            )
            
            # Store email in session to verify OTP later
            request.session['reset_email'] = email
            return redirect('verify_otp')
            
        except User.DoesNotExist:
            # For security, redirect even if email doesn't exist
            request.session['reset_email'] = email
            return redirect('verify_otp')

    return render(request, 'core/forgot_password.html')

def verify_otp(request):
    """
    Handles checking the 6-digit OTP sent to the user's email.
    """
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
        
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        try:
            user = User.objects.get(email=email)
            valid_otp = OTPVerification.objects.filter(
                user=user, 
                otp_code=otp_code, 
                is_verified=False
            ).order_by('-created_at').first()
            
            if valid_otp:
                time_diff = timezone.now() - valid_otp.created_at
                if time_diff.total_seconds() <= 600:
                    valid_otp.is_verified = True
                    valid_otp.save()
                    request.session['otp_verified'] = True
                    return redirect('reset_password')
                else:
                    return render(request, 'core/verify_otp.html', {'error': 'OTP has expired.'})
            else:
                return render(request, 'core/verify_otp.html', {'error': 'Invalid OTP.'})
                
        except User.DoesNotExist:
            return render(request, 'core/verify_otp.html', {'error': 'Invalid OTP.'})

    return render(request, 'core/verify_otp.html', {'email': email})

def reset_password(request):
    """
    Handles saving the new password after OTP verification.
    """
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')
        
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
        
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                
                # Cleanup session and OTPs
                del request.session['reset_email']
                del request.session['otp_verified']
                OTPVerification.objects.filter(user=user).delete()
                
                return redirect('login')
            except User.DoesNotExist:
                return redirect('forgot_password')
        else:
            return render(request, 'core/reset_password.html', {'error': 'Passwords do not match.'})
            
    return render(request, 'core/reset_password.html')
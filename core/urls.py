from django.contrib import admin
from django.urls import path,include
from . import views

# Routing configurations for the core authentication flows and dashboards
urlpatterns = [
    # Auth endpoints
    path('', views.home, name='home'),
    path('signup/',views.userSignupView,name='signup'),
    path('login/',views.userLoginView,name='login'),
    path('logout/',views.userLogoutView,name='logout'),
    
    # Password Reset Flow
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    
    # RBAC specific protected dashboards
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin_dashboard/sync/', views.sync_database_view, name='sync_database'),
    path('resident_dashboard/',views.resident_dashboard,name='resident_dashboard'),
    path('security_dashboard/',views.security_dashboard,name='security_dashboard'),
    
    # Chatbot API
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
]
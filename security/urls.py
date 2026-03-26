from django.urls import path
from . import views

urlpatterns = [
    path('raise/', views.raise_emergency_view, name='raise_emergency'),
    path('dashboard/', views.security_alert_dashboard_view, name='security_alert_dashboard'),
]

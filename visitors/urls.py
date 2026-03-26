from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_visitor_view, name='add_visitor'),
    path('my-visitors/', views.my_visitors_view, name='my_visitors'),
    path('security-log/', views.security_visitor_log_view, name='security_visitor_log'),
]

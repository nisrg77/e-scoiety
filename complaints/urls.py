from django.urls import path
from . import views

urlpatterns = [
    path('raise/', views.raise_complaint_view, name='raise_complaint'),
    path('my-complaints/', views.my_complaints_view, name='my_complaints'),
    path('manage/', views.manage_complaints_view, name='manage_complaints'),
]

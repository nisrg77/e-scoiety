from django.urls import path
from . import views

urlpatterns = [
    path('my-invoices/', views.my_invoices_view, name='my_invoices'),
    path('pay/<int:invoice_id>/', views.pay_invoice_view, name='pay_invoice'),
    path('expenses/', views.expense_report_view, name='expense_report'),
    path('create-invoice/', views.create_invoice_view, name='create_invoice'),
]

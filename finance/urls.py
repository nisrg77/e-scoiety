from django.urls import path
from . import views

urlpatterns = [
    path('my-invoices/', views.my_invoices_view, name='my_invoices'),
    path('pay/<int:invoice_id>/', views.pay_invoice_view, name='pay_invoice'),
    path('expenses/', views.expense_report_view, name='expense_report'),
    path('create-invoice/', views.create_invoice_view, name='create_invoice'),
    path('approve-payment/<int:invoice_id>/', views.approve_payment_view, name='approve_payment'),
    path('reject-payment/<int:invoice_id>/', views.reject_payment_view, name='reject_payment'),
]

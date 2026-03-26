from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.facility_list_view, name='facility_list'),
    path('book/', views.book_facility_view, name='book_facility'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('api/bookings/<int:facility_id>/', views.api_facility_bookings, name='api_facility_bookings'),
    path('pay/<int:booking_id>/', views.pay_booking_view, name='pay_booking'),
    path('cancel/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
]

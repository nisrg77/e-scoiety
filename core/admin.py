from django.contrib import admin
from .models import User, OTPVerification

# Register your models here.
admin.site.register(User)
admin.site.register(OTPVerification)

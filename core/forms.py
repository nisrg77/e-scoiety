from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

# Form to handle user registration validation and creation
class UserSignupForm(UserCreationForm):
    """
    Form to handle new user registration. Inherits from UserCreationForm 
    to provide built-in password validation while extending it for our 
    custom User model fields (email and role).
    """
    class Meta:
        model = User
        # Fields that will be rendered on the signup page
        fields = ['email','role','password1','password2']
        # Widgets to hide the passwords visually in the browser input fields
        widgets = {
            'password1':forms.PasswordInput(),
            'password2':forms.PasswordInput(),
        }

# Simple custom form to authenticate existing users
class UserLoginForm(forms.Form):
    """
    Form to authenticate users for login.
    Takes an email and a password.
    """
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
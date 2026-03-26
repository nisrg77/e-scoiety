from django import forms
from .models import Flat

class ResidentOnboardingForm(forms.Form):
    flat = forms.ModelChoiceField(
        queryset=Flat.objects.all(),
        required=True,
        label="Assign Flat",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    move_in_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

# accounts/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    user_type = forms.ChoiceField(
        choices=[
            ('Teacher', 'Teacher'),
            ('Parent', 'Parent'),
            ('Counselor', 'Counselor'),
            ('IT Admin', 'IT Admin'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

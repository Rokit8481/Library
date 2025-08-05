from django.core.exceptions import ValidationError
from django import forms
from .models import Borrow

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['email', 'birth_date', 'termin']
        widgets = {
            'email': forms.EmailInput(attrs = {'placeholder': 'youremail@example.com'}),
            'birth_date': forms.DateInput(attrs = {'type': 'date'}),
            'termin': forms.Select(attrs = {'aria-label': 'Виберіть термін користування'})
        }
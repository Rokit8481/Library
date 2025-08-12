from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
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

    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('book', None)
        super().__init__(*args, **kwargs)

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        if not birth_date:
            raise ValidationError("Дата народження потрібна.")
            
        today = timezone.now().date() 
        if birth_date >= today:
            raise ValidationError("Ваша дата народження не є можливою!")
            
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise ValidationError("Ви занадто молодий!")
            
        return birth_date
from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model  = Reservation
        fields = ['table', 'datetime', 'number_of_people', 'status']
        widgets = {
            'datetime':       forms.DateTimeInput(attrs={'type':'datetime-local','class':'form-control'}),
            'table':          forms.Select(attrs={'class':'form-select'}),
            'number_of_people': forms.NumberInput(attrs={'class':'form-control'}),
            'status':         forms.Select(attrs={'class':'form-select'}),
        }

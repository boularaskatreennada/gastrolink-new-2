from django import forms
from .models import *

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Restaurant name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'address': forms.Textarea(attrs={'class': 'text-area form-control', 'placeholder': 'Complete address'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control d-none', 'id': 'id_photo'}),
        }

ROLE_CHOICES = [
    ('manager', 'Manager'),
    ('supplier', 'Supplier'),
]
STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
]

class EmployeeForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(required=False ,widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    restaurant = forms.ModelChoiceField(
        queryset=Restaurant.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Restaurant'})
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If data was submitted
        if 'role' in self.data:
            role = self.data.get('role')
            if role == 'manager':
                self.fields['password'].required = True
                self.fields['restaurant'].required = True
                self.fields['status'].required = True
                self.fields['address'].required = False
            elif role == 'supplier':
                self.fields['address'].required = True
                self.fields['password'].required = False
                self.fields['restaurant'].required = False
                self.fields['status'].required = False


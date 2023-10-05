from django import forms
from .models import Customer, TailoringService, Location  # Location modelini ekleyin
from django.forms import DateInput

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'land', 'straat', 'huisnummer','stad', 'bus', 'postcode', 'wedding_date', 'location', 'is_pickup', 'description','services','productvoorraadnummer', 'jasmaat', 'vestmaat', 'broekmaat']
        widgets = {
            'wedding_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.all()  # Dinamik lokasyonlar

class TailoringServiceForm(forms.ModelForm):
    class Meta:
        model = TailoringService
        fields = ['name', 'price']

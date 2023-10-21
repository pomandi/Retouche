from django import forms
from .models import Customer, TailoringService, Location  # Location modelini ekleyin
from django.forms import DateInput

class CustomerForm(forms.ModelForm):
    service_type = forms.ChoiceField(
        choices=Customer.SERVICE_CHOICES,
        required=True,
        initial=None
    )
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(initial='+31',required=True)
    wedding_date = forms.DateField(required=True, widget=DateInput(attrs={'type': 'date'}))
    is_pickup = forms.BooleanField(required=False)

    class Meta:
        model = Customer
        fields = ['service_type', 'name', 'email', 'phone', 'land', 'straat', 'huisnummer', 'stad', 'bus', 'postcode', 'wedding_date', 'location', 'is_pickup', 'description', 'services', 'productvoorraadnummer', 'jasmaat', 'vestmaat', 'broekmaat']


    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.all()  # Dinamik lokasyonlar

class TailoringServiceForm(forms.ModelForm):
    class Meta:
        model = TailoringService
        fields = ['name', 'price']

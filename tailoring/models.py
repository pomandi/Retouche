from django.db import models
import uuid


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TailoringService(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

class Customer(models.Model):
    SERVICE_CHOICES = [
        ('', '---------'),  # Boş bir seçenek ekleyin
        ('Order', 'Order'),
        ('Tailoring', 'Tailoring Service'),
    ]
    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_CHOICES,
        default='',
        blank=False,
        null=False
    )
    tracking_id = models.UUIDField(default=uuid.uuid4, unique=False, editable=False, null=True)
    order_ready = models.BooleanField(default=False)  # Siparişin hazır olup olmadığını belirtir
    services = models.ManyToManyField('TailoringService', blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    unique_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    land = models.CharField(max_length=50, null=True, blank=True)
    straat = models.CharField(max_length=100, null=True, blank=True)
    huisnummer = models.CharField(max_length=10, null=True, blank=True)
    bus = models.CharField(max_length=10, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    stad = models.CharField(max_length=50, null=True, blank=True)
    productvoorraadnummer = models.CharField(max_length=50, null=True, blank=True)
    jasmaat = models.IntegerField(null=True, blank=True)
    vestmaat = models.IntegerField(null=True, blank=True)
    broekmaat = models.IntegerField(null=True, blank=True)
    wedding_date = models.DateField(null=True, blank=True)
    is_pickup = models.BooleanField(default=False)
    email_content = models.TextField(null=True, blank=True, default="Your order has been prepared, please make your appointment via this link https://booking.appointy.com/nl-NL/pomandi/locations.")
    sms_content = models.TextField(null=True, blank=True, default="Your order has been prepared, please make your appointment via this link https://booking.appointy.com/nl-NL/pomandi/locations.")
    description = models.TextField(null=True, blank=True)
    test_field = models.CharField(max_length=100, null=True, blank=True)
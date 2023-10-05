from django.db import models

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
    services = models.ManyToManyField('TailoringService')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    unique_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    land = models.CharField(max_length=50)
    straat = models.CharField(max_length=100)
    huisnummer = models.CharField(max_length=10)
    bus = models.CharField(max_length=10)
    postcode = models.CharField(max_length=10)
    stad = models.CharField(max_length=50)
    productvoorraadnummer = models.CharField(max_length=50, null=True, blank=True)
    jasmaat = models.IntegerField(null=True, blank=True)
    vestmaat = models.IntegerField(null=True, blank=True)
    broekmaat = models.IntegerField(null=True, blank=True)
    wedding_date = models.DateField(null=True, blank=True)
    is_pickup = models.BooleanField(default=False)
    email_content = models.TextField(null=True, blank=True, default="Varsayılan e-posta içeriği burada.")
    sms_content = models.TextField(null=True, blank=True, default="Varsayılan SMS içeriği burada.")
    description = models.TextField(null=True, blank=True)

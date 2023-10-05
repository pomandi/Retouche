from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from .models import Customer, TailoringService, Location
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests


class CustomerAdmin(admin.ModelAdmin):
    change_form_template = 'admin/tailoring/customer_change_form.html'

    list_display = ('name', 'wedding_date', 'location', 'is_pickup', 'email', 'phone')
    fields = ('name', 'wedding_date', 'location', 'is_pickup', 'email', 'phone', 'email_content', 'sms_content','land','straat','huisnummer','bus','postcode','stad','productvoorraadnummer','jasmaat','vestmaat','broekmaat','services', 'description')  # yeni alanlar eklendi
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:object_id>/send_email/', self.admin_site.admin_view(self.send_email), name='tailoring_customer_send_email'),
            path('<int:object_id>/send_sms/', self.admin_site.admin_view(self.send_sms), name='tailoring_customer_send_sms'),
        ]
        return my_urls + urls



    def get_changeform_initial_data(self, request):
        return {'email_content': 'Varsayılan e-posta içeriği burada', 'sms_content': 'Varsayılan SMS içeriği burada'}
    


    def send_email(self, request, object_id):
        customer = Customer.objects.get(pk=object_id)
        email_content = customer.email_content
        
        email = customer.email
        if email_content is None:
            self.message_user(request, f"E-posta içeriği boş, {object_id} numaralı müşteriye e-posta gönderilemedi.")
            return HttpResponseRedirect("..")

        text_message = MIMEText(email_content, 'plain')
        username = 'info@pomandi.com'
        password = 'YU5Z8Ta@KnMHDmC'

        msg = MIMEMultipart('mixed')
        sender = 'info@pomandi.com'  # Gönderici e-posta adresi
        recipient = email  # Müşterinin e-posta adresi

        msg['Subject'] = 'Your Tailoring Service is Ready'
        msg['From'] = sender
        msg['To'] = recipient

        
        msg.attach(text_message)

        mailServer = smtplib.SMTP('mail.smtp2go.com', 2525)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(username, password)
        mailServer.sendmail(sender, recipient, msg.as_string())
        mailServer.close()

        self.message_user(request, f"E-posta {object_id} numaralı müşteriye gönderildi.")
        return HttpResponseRedirect("..")



    def send_sms(self, request, object_id):
        # Müşteri bilgilerini al
        customer = Customer.objects.get(pk=object_id)
        
        phone_number = customer.phone  # Müşterinin telefon numarası

        api_key = "api-8784277C593411EE90A0F23C91BBF4A0"  # SMTP2GO API anahtarı
        destination = [phone_number]  # Müşterinin telefon numarası
        sms_content = customer.sms_content  # SMS içeriği

        # API endpoint
        url = "https://api.smtp2go.com/v3/sms/send"

        # POST isteği için veri
        data = {
            "api_key": api_key,
            "destination": destination,
            "content": sms_content
        }

        # POST isteği gönderme
        response = requests.post(url, json=data)

        if response.status_code == 200:
            self.message_user(request, f"SMS {object_id} numaralı müşteriye gönderildi.")
        else:
            self.message_user(request, "SMS gönderilemedi.")

        return HttpResponseRedirect("..")


admin.site.register(Customer, CustomerAdmin)
admin.site.register(TailoringService)
admin.site.register(Location)

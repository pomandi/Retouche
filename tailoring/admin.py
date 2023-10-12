from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from .models import Customer, TailoringService, Location
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import FileResponse, HttpResponse  
import os
import requests
from io import BytesIO
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.platypus import Spacer


class CustomerAdmin(admin.ModelAdmin):
    change_form_template = 'admin/tailoring/customer_change_form.html'

    list_display = ('service_type','name', 'wedding_date', 'location', 'is_pickup', 'email', 'phone')
    fields = ('unique_id','service_type','name', 'wedding_date', 'location', 'is_pickup', 'email', 'phone', 'email_content', 'sms_content','land','straat','huisnummer','bus','postcode','stad','productvoorraadnummer','jasmaat','vestmaat','broekmaat','services', 'description')  # yeni alanlar eklendi
    readonly_fields = ('unique_id',) 
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:object_id>/send_email/', self.admin_site.admin_view(self.send_email), name='tailoring_customer_send_email'),
            path('<int:object_id>/send_sms/', self.admin_site.admin_view(self.send_sms), name='tailoring_customer_send_sms'),
            path('<int:object_id>/print_pdf/', self.admin_site.admin_view(self.print_pdf), name='tailoring_customer_print_pdf'),  # yeni ekledik

        ]
        return my_urls + urls
    
    def print_pdf(self, request, object_id):
            customer = Customer.objects.get(pk=object_id)
            pdf_data = generate_pdf(customer)
            self.message_user(request, f"PDF {object_id} numaralı müşteri için oluşturuldu.")
            
            response = FileResponse(BytesIO(pdf_data), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{customer.name}.pdf"'
            return response




    def get_changeform_initial_data(self, request):
        return {'email_content': 'Your order has been prepared, please make your appointment via this link https://booking.appointy.com/nl-NL/pomandi/locations ,', 'sms_content': 'Your order has been prepared, please make your appointment via this link https://booking.appointy.com/nl-NL/pomandi/locations ,'}
    


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


def generate_pdf(customer):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        # PDF içeriği
        services = ", ".join([str(service) for service in customer.services.all()])
        location = str(customer.location) if customer.location else "N/A"
    
    # PDF içeriği
        data = [
             
            ["unique_id", customer.unique_id],
            ["Customer Information", ""],
            ["Name", customer.name],
            ["Email", customer.email],
            ["Phone", customer.phone],
            ["Country", customer.land],
            ["Street", customer.straat],
            ["House Number", customer.huisnummer],
            ["Bus Number", customer.bus],
            ["Postal Code", customer.postcode],
            ["City", customer.stad],
            ["Product Stock Number", customer.productvoorraadnummer],
            ["Jacket Size", customer.jasmaat],
            ["Vest Size", customer.vestmaat],
            ["Pants Size", customer.broekmaat],
            ["Wedding Date", customer.wedding_date],
            ["Is Picked Up?", customer.is_pickup],
            ["Email Content", customer.email_content],
            ["SMS Content", customer.sms_content],
            ["Description", customer.description],
            ["Services", services],
            ["Location", location]
        ]

        # Tablo stilini ayarlayın
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Tabloyu oluşturun
        table = Table(data)
        table.setStyle(style)

        # Tablo boyutunu ayarlayın
        table._argW[0] = 9 * cm
        table._argW[1] = 9 * cm

            # QR Kodu oluştur
        whatsapp_url = "https://wa.me/32489107182"
        qr_code = qr.QrCodeWidget(whatsapp_url)
        qr_code.barWidth = 2 * cm
        qr_code.barHeight = 2 * cm
        d = Drawing(50, 50)
        d.add(qr_code)

        # Felemenkçe metin
        whatsapp_text = Paragraph("Als u een vraag heeft over uw bestelling, kunt u contact met ons opnemen via WhatsApp door deze barcode te scannen.", getSampleStyleSheet()["BodyText"])

        # PDF'e ekleyin
        elements = []
        styles = getSampleStyleSheet()
        title_style = styles["Heading1"]
        title_style.alignment = 1  # Merkeze hizala
        elements.append(Paragraph("Customer Information", title_style))
        elements.append(table)
        elements.append(Spacer(1, 20))  # Yükseklik 20 olan bir boşluk ekleyin
        elements.append(d)  # QR kodu ekleyin
        elements.append(Spacer(1, 10))  # Yükseklik 10 olan bir boşluk ekleyin
        elements.append(whatsapp_text)  # Felemenkçe metni ekleyin

        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf






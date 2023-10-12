from django.shortcuts import render, redirect
from .forms import CustomerForm, TailoringServiceForm
from .models import TailoringService,Customer
from django.core.mail import send_mail
from twilio.rest import Client
from django.shortcuts import get_object_or_404
from django.utils import translation
from django.http import HttpResponseRedirect
from django.conf import settings
import requests
from datetime import date, timedelta

def customer_create_view(request):
    form = CustomerForm(request.POST or None)
    urgent_weddings = False  # Yeni bir değişken oluşturun
    total_price = 0

    if form.is_valid():
        customer = form.save(commit=False)
        selected_services = request.POST.getlist('services')
        
        for service_id in selected_services:
            service = TailoringService.objects.get(id=service_id)
            total_price += service.price

        customer.total_price = total_price
        customer.save()
        customer.services.set(selected_services)

        # Düğün tarihi kontrolü
        if customer.wedding_date and customer.wedding_date <= date.today() + timedelta(days=10):
            urgent_weddings = True  # Eğer düğün tarihi 10 gün veya daha azsa, değişkeni True yapın

        # send_notifications(customer)
        return redirect('/tailoring/list/')  # Yönlendirilecek URL

    services = TailoringService.objects.all()
    context = {'form': form, 'services': services, 'total_price': total_price, 'urgent_weddings': urgent_weddings}
    return render(request, 'customer_form.html', context)





# def send_notifications(customer):
#     # Twilio ayarları
#     account_sid = 'TWILIO_ACCOUNT_SID'
#     auth_token = 'TWILIO_AUTH_TOKEN'
#     client = Client(account_sid, auth_token)

#     # SMS gönderme
#     client.messages.create(
#         body='Ürününüz hazır!',
#         from_='+1234567890',  # Twilio telefon numarası
#         to=customer.phone
#     )

#     # E-posta gönderme
#     send_mail(
#         'Ürün Hazır',
#         'Ürününüz hazır ve teslim alınabilir.',
#         'your_email@example.com',
#         [customer.email],
#         fail_silently=False,
#     )



def customer_delete_view(request, id):
    customer = get_object_or_404(Customer, id=id)
    if request.method == 'POST':
        customer.delete()
        return redirect('some-view-name')  # Burada yönlendirilecek görünümü belirtin
    return render(request, 'customer_confirm_delete.html', {'customer': customer})


def customer_list_view(request):
    location_filter = request.GET.get('location', '')
    if location_filter:
        customers = Customer.objects.filter(location=location_filter)
    else:
        customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

def set_language(request):

    import logging
    logger = logging.getLogger(__name__)
    logger.info('set_language function was called')

    user_language = request.GET.get('lang', 'en')  # 'en' varsayılan dil kodudur.
    print("set_language çalıştı")
    if user_language in dict(settings.LANGUAGES).keys():
        translation.activate(user_language)
        request.session['django_language'] = user_language  # Varsayılan dil çerezi adını doğrudan kullandık.
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


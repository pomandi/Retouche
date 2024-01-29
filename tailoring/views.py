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
from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer
from .helpers import send_email, send_sms
from django.utils import timezone


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

        # Set the email_content and sms_content fields after saving the customer.
        tracking_link = f"http://localhost:8000/en/tailoring/order-status/{customer.tracking_id}"
        customer.email_content = f"Track your order here: {tracking_link}"
        customer.sms_content = f"Track your order here: {tracking_link}"
        customer.save()  # Save the customer again to update the email_content and sms_content fields.

        send_email(customer.pk)
        send_sms(customer.pk)
        if customer.wedding_date and customer.wedding_date <= timezone.now().date() + timedelta(days=10):
            urgent_weddings = True  # Eğer düğün tarihi 10 gün veya daha azsa, değişkeni True yapın

        return redirect('/tailoring/list/')  # Yönlendirilecek URL

    services = TailoringService.objects.all()
    context = {'form': form, 'services': services, 'total_price': total_price, 'urgent_weddings': urgent_weddings}
    return render(request, 'customer_form.html', context)








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


def order_ready(request):
    if request.method == 'POST':
        unique_id = request.POST.get('unique_id')
        customer = get_object_or_404(Customer, unique_id=unique_id)
        customer.order_ready = True  # 'order_ready' adında bir alan ekleyin
        customer.save()
        return redirect('customer-list')  # Müşteri listesi sayfasına yönlendir

    return render(request, 'order_ready.html')


def order_status(request, tracking_id):
    customer = get_object_or_404(Customer, tracking_id=tracking_id)
    context = {
        'customer': customer,
    }
    return render(request, 'order_status.html', context)
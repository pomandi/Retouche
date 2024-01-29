from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/en/tailoring/create/', permanent=False)),
]

urlpatterns += i18n_patterns(
    path('tailoring/', include('tailoring.urls')),
    # Diğer URL yapılandırmalarınızı buraya ekleyin
)
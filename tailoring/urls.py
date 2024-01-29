from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.customer_create_view, name='customer-create'),
    path('delete/<int:id>/', views.customer_delete_view, name='customer-delete'),
    path('list/', views.customer_list_view, name='customer-list'),
    path('set_language/', views.set_language, name='set_language'),
    path('order-ready/', views.order_ready, name='order_ready'),
    path('order-status/<uuid:tracking_id>/', views.order_status, name='order_status'),

    


]



from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.place_order, name='checkout'),
    path('order_complete/', views.order_complete, name='order_complete'),
]

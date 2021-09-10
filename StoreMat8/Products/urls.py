from django.urls import path
from .views import *

app_name = 'Products'

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('detail/<slug:slug>/', DetailProduct.as_view(), name='detail'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add-to-cart'),
    path('remove-an-item/<slug:slug>/', remove_an_item_from_cart, name='remove-an-item'),
    path('order-summery/', OrderSummaryView.as_view(), name='order_summery'),
]
from django.urls import path
from .views import *

app_name = 'Products'

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('search_view', SearchProduct.as_view(), name='search'),
    path('detail/<slug:slug>/', DetailProduct.as_view(), name='detail'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-an-item/<slug:slug>/', remove_an_item_from_cart, name='remove-an-item'),
    path('order-summery/', OrderSummaryView.as_view(), name='order_summery'),
]
from django.urls import path
from .views import *

app_name = 'Products'

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('search_view', SearchProduct.as_view(), name='search'),
    path('detail/<slug:slug>/<category>/', DetailProduct.as_view(), name='detail'),
    path('add-to-cart/<slug:slug>/', AddToCart.as_view(), name='add-to-cart'),
    path('remove-from-cart/<slug:slug>/', RemoveFromCart.as_view(), name='remove-from-cart'),
    path('remove-an-item/<slug:slug>/', RemoveAnItemFromCart.as_view(), name='remove-an-item'),
    path('order-summery/', OrderSummaryView.as_view(), name='order_summery'),
]
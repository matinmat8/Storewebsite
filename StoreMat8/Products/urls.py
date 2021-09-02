from django.urls import path
from .views import *

app_name = 'Products'

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add-to-cart'),
]
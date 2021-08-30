from django.shortcuts import render
from django.views import View
from .models import Product


# Show all the products
class index(View):

    def get(self, request):
        products = Product.objects.all()
        return render(request, 'Products/index.html', context={'products': products})
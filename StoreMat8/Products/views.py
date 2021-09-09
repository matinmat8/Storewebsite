from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic.detail import DetailView

from .models import Product, OrderItem, Order


# Show all the products
class index(View):

    def get(self, request):
        products = Product.objects.all()
        return render(request, 'Products/index.html', context={'products': products})


class DetailProduct(DetailView):

    model = Product


def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=product,
        user=request.user,
        ordered=False
    )
    # Get the imported user cart
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item in in order
        if order.items.filter(item__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.Info(request, 'This item quantity was updated.')
            return redirect("Products:index")
        else:
            order.items.add(order_item)
            messages.Info(request, "this item was added to your cart")
            return redirect("Products:index")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.Info(request, "This item was added to your cart.")
        return redirect("Products:index", slug=slug)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'Products/orders_summary.html', context)
        except ObjectDoesNotExist:
            messages.Warning(self.request, "You do not have an active order")
            return redirect("Products:index")
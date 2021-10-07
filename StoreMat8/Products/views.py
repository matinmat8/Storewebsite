from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.postgres.search import SearchVector, SearchQuery
from django.core.checks import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View, TemplateView
from .forms import SearchForm

from .models import Product, OrderItem, Order


# Show all the products
class ProductList(ListView):
    model = Product
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context


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
            return redirect("Products:order_summery")
        else:
            order.items.add(order_item)
            messages.Info(request, "this item was added to your cart")
            return redirect("Products:order_summery")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.Info(request, "This item was added to your cart.")
        return redirect("Products:order_summery", slug=slug)


def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # Get the imported user cart
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                item=product,
                user=request.user,
                ordered=False,
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.Info(request, "This product was removed from your cart!")
            return redirect("Products:order_summery")
        else:
            messages.Info(request, "this product was not in your cart.")
            return redirect("Products:index")
    else:
        messages.Info(request, "You don't have a cart!")
        return redirect("Products:index")  # Redirect to registration page in the future


def remove_an_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # Get the imported user cart
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(
                item=product,
                user=request.user,
                ordered=False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.Info(request, "This item quantity was reduced.")
            return redirect("Products:order_summery")
        else:
            messages.Info(request, "This item was not in your cart.")
            return redirect("Products:order_summery", slug=slug)
    else:
        messages.Info(request, "This item was not in your cart.")
        return redirect("Products:order_summery", slug=slug)


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


class SearchProduct(View):
    form_class = SearchForm
    results = []
    # template_name = "search.html"
    search = None

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        if form.is_valid():
            self.search = form.cleaned_data['search']
            self.results = Product.objects.filter(title=self.search)

        return render(request, 'Products/product_list.html', {'form': form, 'results': self.results, 'search': self.search})



from django import template
from Products.models import Order

register = template.Library()


@register.filter()
def get_final_price(request):
    return Order.get_final(request)


@register.filter()
def get_total_saved_amount(request):
    return Order.total_saved_amount(request)

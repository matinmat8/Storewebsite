from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

STATUS_CHOICES = (
    ('Samsung', 'samsung'),
    ('Apple', 'apple'),
    ('Xiaomi', 'xiaomi'),
    ('Huawei', 'huawei'),
)


class Product(models.Model):
    title = models.CharField(max_length=65)
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True)
    category = models.CharField(max_length=50)
    brand = models.CharField(max_length=10, choices=STATUS_CHOICES)
    image = models.CharField(max_length=300)  # Product cover image url
    slug = models.SlugField()
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("Products:detail", kwargs={
            'slug': self.slug, 'category': self.category,
        })

    def remove_from_cart_url(self):
        return reverse("Products:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def add_to_cart_url(self):
        return reverse("Products:add-to-cart", kwargs={
            'slug': self.slug
        })


class ProductsImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.CharField(max_length=400)  # For image URL form another server

    def __str__(self):
        return f'{self.product, self.image}'


class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.quantity * self.item.price

    def total_discount_price(self):
        return self.quantity * self.item.discount_price

    def saved_amount(self):
        return self.total_price() - self.total_discount_price()

    def final_price(self):
        if self.item.discount_price:
            return self.total_discount_price()
        return self.total_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_final(cls, request):
        total = 0
        o = Order.objects.get(user=request.user)
        order = o.items.all()
        for order_item in order:
            total += order_item.final_price()
        return total

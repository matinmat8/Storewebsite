from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

STATUS_CHOICES = (
    ('Samsung', 'samsung'),
    ('Apple', 'apple'),
    ('Xiaomi', 'xiaomi'),
    ('Huawei', 'huawei'),
)


# App's major categories
class Category(models.Model):
    following_categories = models.ForeignKey('self', on_delete=models.RESTRICT, blank=True, null=True)
    title = models.CharField(max_length=65)
    description = models.TextField()
    
    def get_absolute_url(self):
        return reverse("Products:FollowingCategories", kwargs={
            'pk': self.pk,
        })


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(max_length=65)
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True)
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
            'slug': self.slug, 'pk': self.category.pk,
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

    @classmethod
    def total_saved_amount(cls, request):
        total = 0
        o = Order.objects.get(user=request.user)
        order = o.items.all()
        for order_item in order:
            total += order_item.saved_amount()
        return total


class DiscountSystem(models.Model):
    discount_is_for = models.ForeignKey(User, on_delete=models.CASCADE)
    discount_code = models.CharField(max_length=50)
    discount_percent = models.FloatField()
    due_date = models.DateField()

    def __str__(self):
        return self.discount_is_for.username
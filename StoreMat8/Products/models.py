from django.db import models

# Create your models here.

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
    slug = models.SlugField()

    def __str__(self):
        return f"{self.title}"

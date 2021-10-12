from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    price_netto = models.DecimalField(decimal_places=2, max_digits=10000)
    VAT_VALUE = (
        (1, "0,23"),
        (2, "0,08"),
        (3, "0,05"),
        (4, "0")
    )
    vat = models.FloatField(choices=VAT_VALUE)
    code_EAN = models.IntegerField()
    SKU = models.IntegerField(unique=True)
    in_stock = models.BooleanField(default=False)
    expire_date = models.DateField(null=True)
    img = models.ImageField()
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', args=(self.pk,))

    # def get_delete_url(self):
    #     return reverse('delete-product', args=(self.pk,))
    #
    # def get_edit_url(self):
    #     return reverse('edit-product', args=(self.pk,))


class Category(models.Model):
    name = models.CharField(max_length=64)
    products = models.ManyToManyField(Product)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-details', args=(self.pk,))

    # def get_delete_url(self):
    #     return reverse('delete-category', args=(self.pk,))
    #
    # def get_edit_url(self):
    #     return reverse('edit-category', args=(self.pk,))


class Discount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, primary_key=True)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user} Discount 20%: {self.is_active}"


class Cart(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    price = models.FloatField(default=0)
    def __str__(self):
        return f'{self.user.username} {self.user_id}'


class Delivery(models.Model):
    name = models.CharField(max_length=64)
    DELIVERY_METHODS = (
        (1, "za pobraniem"),
        (2, "przelewem"),
        (3, "voucherem")
    )
    delivery_method = models.IntegerField(choices=DELIVERY_METHODS, default=1)
    def __str__(self):
        return self.name


class Payment(models.Model):
    payment_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=64)
    is_done = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Order(models.Model):
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE, default=-1)
    order_id = models.IntegerField(auto_created=True, unique=True)
    delivery_method = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, primary_key=True)
    user_id = models.ManyToOneRel("Order", on_delete=models.CASCADE, to=User, field_name="name")
    price = models.FloatField()
    is_payed = models.BooleanField(default=False)
    in_completing = models.BooleanField(default=False)
    is_send = models.BooleanField(default=False)
    in_delivery_done = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.order_id}'

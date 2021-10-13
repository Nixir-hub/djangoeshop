from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.urls import reverse


class CustomerUser(User):
    class Meta:
        permissions = (
            ('permission_cart_view', 'Watch self cart'),
        )

    def save(self, *args, **kwargs):
        super(User, self).save(self, *args, **kwargs)
        discount = Discount.objects.create(user=User.objects.get(id=self.pk), amount=0.3)
        discount.save()
        Cart.objects.create(id=self.pk, discount=discount, user=User.objects.get(id=self.pk)).save()

    def get_delete_url(self):
        return reverse('delete-user', args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit-user', args=(self.pk,))

    def get_edit_pass_url(self):
        return reverse('password_change')


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    price_netto = models.FloatField()
    VAT_VALUE = (
        (1, "0.23"),
        (2, "0.08"),
        (3, "0.05"),
        (4, "0")
    )
    vat = models.FloatField(choices=VAT_VALUE, default=4)
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
    def add_to_cart(self):
        return reverse('add_to_cart', args=(self.pk,))


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
    is_active = models.BooleanField(default=True)
    amount = models.FloatField()

    def __str__(self):
        return f"{self.user} Discount {str(self.amount * 100) + '%' }: {self.is_active}"


class Cart(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product,
        related_name='carts',
        through='CartProduct'
    )

    def __str__(self):
        return f'{self.user.username},numer id koszyka= {self.user_id}'


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
           models.UniqueConstraint(fields=['product', 'cart'], name='unique_product_cart')

    def __str__(self):
        return f"{self.product}"

    def get_absolute_url(self):
        return reverse('product-detail', args=(self.pk,))

    def get_delete_url(self):
        return reverse('delete-cart-product', args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit-cart-product', args=(self.pk,))


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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    is_payed = models.BooleanField(default=False)
    in_completing = models.BooleanField(default=False)
    is_send = models.BooleanField(default=False)
    in_delivery_done = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.order_id}'

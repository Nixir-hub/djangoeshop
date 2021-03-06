from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.urls import reverse
from sorl.thumbnail import ImageField, get_thumbnail


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adres = models.CharField(max_length=255, null=True)
    company_adres = models.TextField(null=True)
    phone = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profil-view', args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit-user', args=(self.pk,))


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    stock = models.PositiveIntegerField()
    price_netto = models.FloatField()
    categories = models.ManyToManyField("Category")
    VAT_VALUE = (
        (1, "0.23"),
        (2, "0.08"),
        (3, "0.05"),
        (4, "0")
    )
    vat = models.FloatField(choices=VAT_VALUE, default=4)
    SKU = models.IntegerField(unique=True, null=True)
    in_stock = models.BooleanField(default=False)
    expire_date = models.DateField(null=True)
    img = ImageField(upload_to='photos', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_brutto_price(self):
        brutto = self.price_netto + float(self.get_vat_display()) * self.price_netto
        return round(brutto, 2)

    def get_procent_vat(self):
        vat = str(float(self.get_vat_display()) * 100) + "%"
        return vat

    def get_category_url(self):
        return reverse('category-details', args=(self.categories.self.category.pk,))

    def get_absolute_url(self):
        return reverse('product-detail', args=(self.pk,))

    def add_to_cart(self):
        return reverse('add_to_cart', args=(self.pk,))

    def get_delete_url(self):
        return reverse("delete-product", args=(self.pk,))

    def get_edit_url(self):
        return reverse("edit-product", args=(self.pk,))

    def save(self, *args, **kwargs):
        if self.img:
            self.image = get_thumbnail(self.img, '500x600', quality=99, format='JPEG')
        super(Product, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=64)
    img = ImageField(upload_to='photos', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-details', args=(self.pk,))

    def get_delete_url(self):
        return reverse('delete-category', args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit-category', args=(self.pk,))

    def save(self, *args, **kwargs):
        if self.img:
            self.image = get_thumbnail(self.img, '500x600', quality=99, format='JPEG')
        super(Category, self).save(*args, **kwargs)


class Discount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    amount = models.FloatField()

    def __str__(self):
        return f"Zni??ka {str(self.amount * 100) + '%'}"


class Cart(models.Model):
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product,
        related_name='carts',
        through='CartProduct'
    )

    def __str__(self):
        return f'{self.user.username},numer id koszyka= {self.user_id}'

    def get_summary_vat(self):
        products = self.cartproduct_set.all()
        summary_vat = 0
        for product in products:
            summary_vat += product.quantity * (
                        product.product.price_netto * float(product.product.get_vat_display()))
        return round(summary_vat, 2)

    def get_summary_netto(self):
        products = self.cartproduct_set.all()
        netto_summary_price = 0
        for product in products:
            netto_summary_price += product.product.price_netto * product.quantity
        return round(netto_summary_price, 2)

    def get_summary_brutto(self):
        products = self.cartproduct_set.all()
        brutto_summary_price = 0
        for product in products:
            brutto_summary_price += product.quantity * (
                product.product.price_netto + product.product.price_netto * float(product.product.get_vat_display()))
        return round(brutto_summary_price, 2)

    def get_summary_brutto_after_discount(self):
        products = self.cartproduct_set.all()
        brutto_summary_price = 0
        for product in products:
            brutto_summary_price += \
                product.quantity * \
                (product.product.price_netto + product.product.price_netto * float(product.product.get_vat_display()))
        return round(brutto_summary_price - brutto_summary_price * self.user.discount_set.first().amount, 2)


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
        return reverse("delete-cart-product", args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit-cart-product', args=(self.pk,))

    def add_quantity(self):
        return reverse("add_to_cart", args=(self.product.id,))

    def remove_quantity(self):
        return reverse("edit-cart-product", args=(self.product.pk,))


class Delivery(models.Model):
    name = models.CharField(max_length=64)
    DELIVERY_METHODS = (
        (1, "za pobraniem"),
        (2, "przelewem"),
        (3, "voucherem")
    )
    delivery_method = models.IntegerField(choices=DELIVERY_METHODS, default=1)

    def get_absolute_url(self):
        return reverse('delivery-detail', args=(self.pk,))

    def get_delete_url(self):
        return reverse('delete-delivery', args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit-delivery', args=(self.pk,))

    def __str__(self):
        return self.name


class Payment(models.Model):
    name = models.CharField(max_length=64)
    is_done = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('payment-detail', args=(self.pk,))

    def get_delete_url(self):
        return reverse('delete-payment', args=(self.pk,))

    def get_edit_url(self):
        return reverse('edit-payment', args=(self.pk,))

    def __str__(self):
        return self.name


class Order(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default=-1)
    order = models.IntegerField(unique=True)
    delivery_method = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.TextField(null=True)
    price = models.FloatField()
    is_payed = models.BooleanField(default=False)
    in_completing = models.BooleanField(default=False)
    is_send = models.BooleanField(default=False)
    in_delivery_done = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('order-detail', args=(self.pk,))

    def __str__(self):
        return f' {self.order}'

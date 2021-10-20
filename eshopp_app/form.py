from django import forms
from eshopp_app.models import Order, Product, Category, Delivery, Payment


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("payment", "delivery_method")


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("expire_date",)


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class AddDeliverForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = "__all__"


class AddPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"

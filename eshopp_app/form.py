from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User

from eshopp_app.models import Order, Product, Category, Delivery, Payment


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        form = "signup.html"
        fields = ('username', "first_name", "last_name", "email", 'password1', 'password2')


class PasswordChangeForm(SetPasswordForm):
    class Meta:
        model = User
        form = "password_change_form.html"
        fields = ('old_password', 'new_password1', 'new_password2')
        labels = {
            ""
        }


class EditProfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


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

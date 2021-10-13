from django import  forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from eshopp_app.models import Cart, Discount, CustomerUser, CartProduct, Product


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomerUser
        fields = ('username', 'password1', 'password2', )


class UpdateCartForm(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = ["quantity", "product", "cart"]

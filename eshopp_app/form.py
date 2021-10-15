from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from eshopp_app.models import CartProduct, Order


class LoginForm(forms.Form):
    username = forms.CharField(label=("Nazwa użytkownika"))
    password = forms.CharField(label=("Hasło"), widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        form = "signup.html"
        fields = ('username', "first_name", "last_name", "email", 'password1', 'password2')





# class PasswordChangeForm(SetPasswordForm):
#     class Meta:
#         model = User
#         fields = ('old_password', 'new_password1', 'new_password2')


class UpdateCartForm(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = ("quantity",)


class EditProfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

from django import forms
from django.contrib.auth.forms import UserCreationForm


from eshopp_app.models import CustomerUser, CartProduct, Order


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomerUser
        fields = ('username', 'password1', 'password2', )


# class PasswordChangeForm(SetPasswordForm):
#     class Meta:
#         model = User
#         fields = ('old_password', 'new_password1', 'new_password2')


class UpdateCartForm(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = ["quantity", "product", "cart"]


class EditProfilForm(forms.ModelForm):
    class Meta:
        model = CustomerUser
        fields = "__all__"


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("delivery_method", "payment_id")
        # exclude = ("is_payed", "in_completing", "is_send", "in_delivery_done", "user_id", "cart_id", "order_id",)

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from eshopp_app.form import SignUpForm, UpdateCartForm, CreateOrderForm
from eshopp_app.models import Product, Category, Cart, CartProduct, Order, Discount, Profile


class MainMenuView(View):
    def get(self, request):
        return render(request, "base.html")


class ProductsListView(ListView):
    model = Product
    template_name = "product_list.html"


class ProductDetailsView(DetailView):
    model = Product
    template_name = "product_detail.html"


class CategoriesListView(ListView):
    model = Category
    template_name = "product_list.html"


class CategoryDetailsView(DetailView):
    model = Category
    template_name = "category_detail.html"


class CartDetailsView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = "cart_detail.html"

    def get_object(self, queryset=None):
        self.object = self.request.user.cart
        return self.object


class CartProductCreateView(LoginRequiredMixin, CreateView):
    model = CartProduct
    form_class = UpdateCartForm
    template_name = "form.html"
    success_url = f"/"

    def form_valid(self, form):
        form.instance.quantity = 1
        return super().form_valid(form)


class EditCartProductView(LoginRequiredMixin, UpdateView):
    model = CartProduct
    fields = ("quantity",)
    template_name = "form.html"
    success_url = f"/"


class DelCartProductView(LoginRequiredMixin, DeleteView):
    model = CartProduct
    template_name = "form.html"
    success_url = f"/"


class UserProfilView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profil_detail.html"

    def get_object(self, queryset=None):
        self.object = self.request.user.profile
        return self.object


class CreateUser(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "form.html"
    success_url = "/login"

    def get_success_url(self):
        obj = self.get_object()
        discount = Discount.objects.create(user=obj, amount=0.3).save()
        Cart.objects.create(discount=discount, user=obj).save()
        return reverse("/login")


class DeleteCustomerUser(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "form.html"
    success_url = "/"


class EditCustomerUserProfil(LoginRequiredMixin, UpdateView):
    model = User
    fields = ("first_name", "last_name", "email", "adres", "phone")
    template_name = "form.html"

    def get_success_url(self):
        obj = self.get_object()
        return reverse("profil-view", args=(obj.id,))


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "order_details.html"


class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = "form.html"
    form_class = CreateOrderForm
    success_url = "/"


# class PasswordChangeView(PasswordContextMixin, FormView):
#     model = User
#     form_class = PasswordChangeForm
#     template_name = "form.html"
#     success_url = "/"

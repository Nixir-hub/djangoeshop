from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from eshopp_app.form import SignUpForm, UpdateCartForm, CreateOrderForm, LoginForm, PasswordChangeForm
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
    fields = "__all__"
    template_name = "form.html"
    success_url = f"/"


class DelCartProductView(LoginRequiredMixin, DeleteView):
    model = CartProduct
    template_name = "del_prod_from_cart_form.html"
    success_url = f"/cart"


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


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "del_form.html"
    success_url = "/"


class EditUserProfil(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ("adres", "phone")
    template_name = "form.html"
    success_url = "/profil_details/"


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "order_details.html"


class CreateOrderView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = "form.html"
    form_class = CreateOrderForm
    success_url = "/"


class PasswordChangeView(FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = "form.html"
    success_url = "/"

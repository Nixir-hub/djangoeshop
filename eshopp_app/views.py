from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from eshopp_app.form import SignUpForm, UpdateCartForm
from eshopp_app.models import Product, Category, Cart, CustomerUser, CartProduct


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


class CartDetailsView(DetailView):
    model = Cart
    template_name = "cart_detail.html"


class CartProductCreateView(CreateView):
    model = CartProduct
    form_class = UpdateCartForm
    template_name = "form.html"
    success_url = f"/"


class CreateUser(CreateView):
    model = CustomerUser
    form_class = SignUpForm
    template_name = "form.html"
    success_url = "/login"



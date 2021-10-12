from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from eshopp_app.models import Product, Category, Cart


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
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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


class CartDetailsView(View):
    def get(self, request, pk):
        cart = Cart.objects.get(id=pk)
        products = cart.cartproduct_set.all()
        netto_summary_price = 0
        brutto_summary_price = 0
        summary_vat = 0
        for product in products:
             netto_summary_price += product.product.price_netto * product.quantity
             brutto_summary_price += product.quantity * (product.product.price_netto + product.product.price_netto * float(product.product.get_vat_display()))
             summary_vat += product.quantity * (product.product.price_netto * float(product.product.get_vat_display()))
        return render(request, "cart_detail.html", {"cart": cart,
                                                    "netto_summary": netto_summary_price,
                                                    "brutto_summary": brutto_summary_price,
                                                    "summary_vat": summary_vat
                                                    })


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


class EditCartProductView(UpdateView):
    model = CartProduct
    fields = ("quantity",)
    template_name = "form.html"
    success_url = f"/"


class DelCartProductView(DeleteView):
    model = CartProduct
    template_name = "form.html"
    success_url = f"/"

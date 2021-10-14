from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from eshopp_app.form import SignUpForm, UpdateCartForm, CreateOrderForm
from eshopp_app.models import Product, Category, Cart, CustomerUser, CartProduct, Order


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

    def form_valid(self, form):
        form.instance.quantity = 1
        return super().form_valid(form)


class EditCartProductView(UpdateView):
    model = CartProduct
    fields = ("quantity",)
    template_name = "form.html"
    success_url = f"/"


class DelCartProductView(DeleteView):
    model = CartProduct
    template_name = "form.html"
    success_url = f"/"


class UserProfilView(DetailView):
    model = CustomerUser
    template_name = "profil_detail.html"


class CreateUser(CreateView):
    model = CustomerUser
    form_class = SignUpForm
    template_name = "form.html"
    success_url = "/login"


class DeleteCustomerUser(DeleteView):
    model = CustomerUser
    template_name = "form.html"
    success_url = "/"


class EditCustomerUserProfil(UpdateView):
    model = CustomerUser
    fields = ("username", "first_name", "last_name", "email", "adres", "phone")
    template_name = "form.html"
    success_url = "/"


class OrderDetailView(DetailView):
    model = Order
    template_name = "order_details.html"


class CreateOrderView(CreateView):
    model = Order
    template_name = "form.html"
    form_class = CreateOrderForm
    success_url = "/"


# class PasswordChangeView(PasswordContextMixin, FormView):
#     model = User
#     form_class = PasswordChangeForm
#     template_name = "form.html"
#     success_url = "/"

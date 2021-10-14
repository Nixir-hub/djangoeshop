from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.views import PasswordContextMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from eshopp_app.form import SignUpForm, UpdateCartForm, CreateOrderForm
from eshopp_app.models import Product, Category, Cart, CustomerUser, CartProduct, Order, Payment, Delivery


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
        if cart.discount.is_active == True:
            summary_after_discount = brutto_summary_price - brutto_summary_price * cart.discount.amount
            return render(request, "cart_detail.html", {"cart": cart,
                                                    "netto_summary": netto_summary_price,
                                                    "brutto_summary": brutto_summary_price,
                                                    "summary_vat": summary_vat,
                                                    "after_discount": summary_after_discount
                                                    })
        return render(request, "cart_detail.html", {"cart": cart,
                                                    "netto_summary": netto_summary_price,
                                                    "brutto_summary": brutto_summary_price,
                                                    "summary_vat": summary_vat,
                                                    })


class CartProductCreateView(CreateView):
    model = CartProduct
    form_class = UpdateCartForm
    template_name = "form.html"
    success_url = f"/"


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
    model = User
    template_name = "form.html"


class EditCustomerUserProfil(UpdateView):
    model = User
    fields = ("username", "first_name", "last_name", "email")
    template_name = "form.html"
    success_url = "/"


class OrderDetailView(DetailView):
    model = Order
    template_name = "order_details.html"



# class PasswordChangeView(PasswordContextMixin, FormView):
#     model = User
#     form_class = PasswordChangeForm
#     template_name = "form.html"
#     success_url = "/"


class CreateOrderView(View):
    def get(self, request):
        form = CreateOrderForm
        return render(request, "form.html", {"form": form})

    def post(self, request):
        payment = Payment.objects.get(id=int(request.POST.get("payment_id")))
        delivery = Delivery.objects.get(id=int(request.POST.get("delivery_method")))
        cart = Cart.objects.get(id=2)
        user = User.objects.get(id=int(cart.user.id))
        order_id = len(user.order_set.all()) + 1
        products = cart.cartproduct_set.all()
        brutto_summary_price =0
        for product in products:
            brutto_summary_price += product.quantity * (product.product.price_netto + product.product.price_netto * float(
                    product.product.get_vat_display()))
        order = Order.objects.create(payment_id=payment,
                                     order_id=order_id,
                                     user_id=user,
                                     delivery_method=delivery,
                                     cart_id=Cart.objects.get(id=cart.id),
                                     price=brutto_summary_price,
                                     cart_id_id= cart.id
                                     )
        order.save()
        return redirect("/")
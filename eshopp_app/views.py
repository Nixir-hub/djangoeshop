from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from eshopp_app.form import SignUpForm, CreateOrderForm, PasswordChangeForm, AddProductForm, AddCategoryForm, \
    AddDeliverForm, AddPaymentForm
from eshopp_app.models import Product, Category, Cart, CartProduct, Order, Discount, Profile, Payment, Delivery


# 2 tests on
class MainMenuView(View):
    def get(self, request):
        return render(request, "base.html", )


# 2 tests on
class SearchResultsView(ListView):
    model = Product
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(name__icontains=query) | Q(categories__name__icontains=query)
        )
        return object_list


# 2 test #
class ProductsListView(ListView):
    model = Product
    template_name = "product_list.html"
    paginate_by = 25
    queryset = Product.objects.filter().order_by("-name").order_by("-in_stock")


# 2 testy
class ProductDetailsView(DetailView):
    model = Product
    template_name = "product_detail.html"


# 4testy
class AddProductView(PermissionRequiredMixin, CreateView):
    permission_required = "eshopp_app.add_product"
    model = Product
    form_class = AddProductForm
    template_name = "form.html"
    success_url = "/products"


# 3 Testy 1post nie przepuszcza przez img prawdopodobnie
class EditProductView(PermissionRequiredMixin, UpdateView):
    permission_required = "eshopp_app.change_product"
    permission_denied_message = "Nie masz uprawnień"
    model = Product
    form_class = AddProductForm
    template_name = "form.html"
    success_url = "/products"


# 4testy
class DeleteProductView(PermissionRequiredMixin, DeleteView):
    permission_required = "eshopp_app.delete_product"
    permission_denied_message = "Nie masz uprawnień"
    model = Product
    template_name = "del_product_form.html"
    success_url = "/products"


#  2 test
class CategoriesListView(ListView):
    model = Category
    template_name = "category_list.html"
    paginate_by = 4
    queryset = Category.objects.filter().order_by('-name')


# Tu mam 1 test czy sprawdzać empty?
class CategoryDetailsView(DetailView):
    model = Category
    template_name = "category_detail.html"
    queryset = Category.objects.all().filter().order_by('-name').order_by("-product__in_stock")


# 2 testy na get 1 na post
class AddCategoryView(PermissionRequiredMixin, CreateView):
    permission_required = "eshopp_app.add_category"
    permission_denied_message = "Nie masz uprawnień"
    model = Category
    form_class = AddCategoryForm
    template_name = "form.html"
    success_url = "/categories"


# 2 testy na get, 1 post
class EditCategoryView(PermissionRequiredMixin, UpdateView):
    permission_required = "eshopp_app.change_category"
    permission_denied_message = "Nie masz uprawnień"
    model = Category
    form_class = AddCategoryForm
    template_name = "form.html"
    success_url = "/categories"


# 4 testy zrobione
class DeleteCategoryView(PermissionRequiredMixin, DeleteView):
    permission_required = "eshopp_app.delete_category"
    permission_denied_message = "Nie masz uprawnień"
    model = Category
    template_name = "del_category_form.html"
    success_url = "/categories"


# 2 testy zrobione
class CartDetailsView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = "cart_detail.html"

    def get_object(self, queryset=None):
        self.object = self.request.user.cart
        return self.object


# 2 testy get
class CartProductCreateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        user = self.request.user

        try:
            cart_product = CartProduct.objects.get(product=product, cart=user.cart)
            cart_product.quantity +=1
            cart_product.save()
            return redirect("/cart")
        except Exception:
            self.creation = CartProduct.objects.create(cart=user.cart, product=product, quantity=1)
            return redirect("/cart")


# 3 testy get
class RemoveCartProductView(LoginRequiredMixin, View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        user = self.request.user
        try:
            cart_product = CartProduct.objects.get(product=product, cart=user.cart)
            cart_product.quantity -= 1
            if cart_product.quantity == 0:
                cart_product.delete()
                return redirect("/cart")
            cart_product.save()
            return redirect("/cart")
        except Exception:
            cart_product = CartProduct.objects.get(product=product, cart=user.cart)
            cart_product.delete()
            return redirect("/cart")


# 2 testy get
class DelCartProductView(UserPassesTestMixin, View):
    def test_func(self):
        pk = self.kwargs['pk']
        try:
            self.model.objects.get(cart=self.request.user.cart, pk=pk)
            return True
        except self.model.DoesNotExist:
            return False
    model = CartProduct
    success_url = "/cart/"

    def get(self, request, pk):
        cart_product = CartProduct.objects.get(id=pk)
        cart_product.delete()
        return redirect("/cart/")


# 2 TESTY zrobione
class UserProfilView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profil_detail.html"

    def get_object(self, queryset=None):
        self.object = self.request.user
        return self.object


# test 1 get 1 post
class CreateUser(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, "registration/signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(username=request.POST.get("username"),
                                       first_name=request.POST.get("first_name"),
                                       last_name=request.POST.get("last_name"),
                                       email=request.POST.get("email"))
            user.set_password(request.POST.get("password1"))
            user.save()
            discount = Discount.objects.create(user=User.objects.get(id=user.id), amount=0.3)
            discount.save()
            Cart.objects.create(user=User.objects.get(id=user.id), discount=Discount.objects.get(user=User.objects.get(id=user.id))).save()
            Profile.objects.create(user=User.objects.get(id=user.id)).save()
            return redirect("/logout")
        return render(request, 'form.html', {'form': form})


# 2 testy na get 1 test z postem
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "del_form.html"
    success_url = "/"

    def get_object(self, queryset=None):
        self.object = self.request.user
        return self.object


# 3 testy 2 get, 1 post
class EditUserProfil(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ("adres", "phone")
    template_name = "form.html"
    success_url = "/profil_details/"

    def get_object(self, queryset=None):
        self.object = self.request.user.profile
        return self.object


# 3 testy 2 get 1 post
class EditUserData(LoginRequiredMixin, UpdateView):
    model = User
    fields = ("first_name", "last_name")
    template_name = "form.html"
    success_url = "/profil_details/"

    def get_object(self, queryset=None):
        self.object = self.request.user
        return self.object


# 2 testy get
class OrderDetailView(UserPassesTestMixin, DetailView):

    def test_func(self):
        pk = self.kwargs['pk']
        try:
            self.model.objects.get(user=self.request.user, pk=pk)
            return True
        except self.model.DoesNotExist:
            return False
    model = Order
    template_name = "order_details.html"


# TODO: create accounts_app
# 6 testów 3 get 3 post
class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request):
        object = self.request.user
        if len(object.cart.cartproduct_set.all()) == 0:
            return redirect("/cart")
        for cartproduct in object.cart.cartproduct_set.all():
            cart_product = object.cart.cartproduct_set.get(
                product=Product.objects.get(id=cartproduct.product.id))
            # TODO:wyświetlanie alertu
            if cartproduct.product.stock < cart_product.quantity:
                return redirect("/cart/", context={"alert":"Nie ma tyle produktu na stanie"})
            else:
                form = CreateOrderForm()
                return render(request, "form.html", {"form": form})
        form = CreateOrderForm()
        return render(request, "form.html", {"form": form})

    def post(self, request):
        object = self.request.user
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            if object.cart.discount.is_active:
                if Payment.objects.get(pk=int(request.POST.get("payment"))).is_done:
                    order = Order.objects.create(payment=Payment.objects.get(pk=int(request.POST.get("payment"))),
                            order=(Order.objects.last().order+1),
                            delivery_method=Delivery.objects.get(id=request.POST.get("delivery_method")),
                            user=object,
                            price=object.cart.get_summary_brutto_after_discount(),
                            is_payed=True
                             )
                    order.save()
                    discount = object.cart.discount
                    discount.is_active = False
                    discount.save()
                    for cartproduct in object.cart.cartproduct_set.all():
                        cart_product = object.cart.cartproduct_set.get(
                            product=Product.objects.get(id=cartproduct.product.id))
                        if cartproduct.product.stock > 0:
                            cartproduct.product.stock = cartproduct.product.stock - cart_product.quantity
                            cartproduct.product.save()
                            if cartproduct.product.stock == 0:
                                cartproduct.product.in_stock = False
                                cartproduct.product.save()
                    object.cart.cartproduct_set.all().delete()
                    return redirect("/profil_details/")
                else:
                    order = Order.objects.create(payment=Payment.objects.get(pk=int(request.POST.get("payment"))),
                                                 order=(Order.objects.last().order + 1),
                                                 delivery_method=Delivery.objects.get(id=request.POST.get("delivery_method")),
                                                 user=object,
                                                 price=object.cart.get_summary_brutto_after_discount(),
                                                 )
                    order.save()
                    discount = object.cart.discount
                    discount.is_active = False
                    discount.save()
                    for cartproduct in object.cart.cartproduct_set.all():
                        cart_product = object.cart.cartproduct_set.get(
                            product=Product.objects.get(id=cartproduct.product.id))
                        if cartproduct.product.stock > 0:
                            cartproduct.product.stock = cartproduct.product.stock - cart_product.quantity
                            cartproduct.product.save()
                            if cartproduct.product.stock == 0:
                                cartproduct.product.in_stock = False
                                cartproduct.product.save()
                    object.cart.cartproduct_set.all().delete()
                    return redirect("/profil_details/")
            elif Payment.objects.get(pk=int(request.POST.get("payment"))).is_done:
                order = Order.objects.create(payment=Payment.objects.get(pk=int(request.POST.get("payment"))),
                            order=(Order.objects.last().order+1),
                            delivery_method=Delivery.objects.get(id=request.POST.get("delivery_method")),
                            user=object,
                            price=object.cart.get_summary_brutto(),
                            is_payed=True
                         )
                order.save()
                for cartproduct in object.cart.cartproduct_set.all():
                    cart_product = object.cart.cartproduct_set.get(
                        product=Product.objects.get(id=cartproduct.product.id))
                    if cartproduct.product.stock > 0:
                        cartproduct.product.stock = cartproduct.product.stock - cart_product.quantity
                        cartproduct.product.save()
                        if cartproduct.product.stock == 0:
                            cartproduct.product.in_stock = False
                            cartproduct.product.save()
                object.cart.cartproduct_set.all().delete()
                return redirect("/profil_details/")
            else:
                order = Order.objects.create(payment=Payment.objects.get(pk=int(request.POST.get("payment"))),
                                             order=(Order.objects.last().order + 1),
                                             delivery_method=Delivery.objects.get(
                                                 id=request.POST.get("delivery_method")),
                                             user=object,
                                             price=object.cart.get_summary_brutto(),
                                             )
                order.save()
                for cartproduct in object.cart.cartproduct_set.all():
                    cart_product = object.cart.cartproduct_set.get(
                        product=Product.objects.get(id=cartproduct.product.id))
                    if cartproduct.product.stock > 0:
                        cartproduct.product.stock = cartproduct.product.stock - cart_product.quantity
                        cartproduct.product.save()
                        if cartproduct.product.stock == 0:
                            cartproduct.product.in_stock = False
                            cartproduct.product.save()
                object.cart.cartproduct_set.all().delete()
                return redirect("/profil_details/")
        else:
            return redirect("/cart/")


# 3 testy 2 get 1 post
class PasswordChangeView(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = "form.html"
    success_url_reverse_lazy = "/profil_details/"


# 3 testy get
class DeliveryListView(PermissionRequiredMixin, ListView):
    permission_required = "eshopp_app.view_delivery"
    model = Delivery
    template_name = "delivery_list.html"
    paginate_by = 25
    queryset = Delivery.objects.filter().order_by('-name')


# 3 testy
class DeliveryDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "eshopp_app.view_delivery"
    model = Delivery
    template_name = "delivery_detail.html"


# 3testy
class AddDeliveryView(PermissionRequiredMixin, CreateView):
    permission_required = "eshopp_app.add_delivery"
    model = Delivery
    form_class = AddDeliverForm
    template_name = "form.html"
    success_url = "/site_moderator/"


# 4testy 3 get 1 post
class EditDeliveryView(PermissionRequiredMixin, UpdateView):
    permission_required = "eshopp_app.change_delivery"
    model = Delivery
    fields = "__all__"
    template_name = "form.html"
    success_url = "/site_moderator/"


# 4 testy 3 get 1 post
class DeleteDeliveryView(PermissionRequiredMixin, DeleteView):
    permission_required = "eshopp_app.delete_delivery"
    model = Delivery
    template_name = "del_delivery_form.html"
    success_url = "/site_moderator/"


# 3 testy get
class PaymentListView(PermissionRequiredMixin, ListView):
    permission_required = "eshopp_app.view_payment"
    model = Payment
    template_name = "payment_list.html"
    paginate_by = 25
    queryset = Payment.objects.filter().order_by('-name')


# 3 testy get
class PaymentDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "eshopp_app.view_payment"
    model = Payment
    template_name = "payment_detail.html"


# 4 test 3 get 1 post
class AddPaymentView(PermissionRequiredMixin, CreateView):
    permission_required = "eshopp_app.add_payment"
    model = Payment
    form_class = AddPaymentForm
    template_name = "payment_form.html"
    success_url = "/site_moderator/"


# 4 testy 3get 1post
class EditPaymentView(PermissionRequiredMixin, UpdateView):
    permission_required = "eshopp_app.change_payment"
    model = Payment
    fields = "__all__"
    template_name = "form.html"
    success_url = "/site_moderator/"


# 4 testy 3 get 1 post
class DeletePaymentView(PermissionRequiredMixin, DeleteView):
    permission_required = "eshopp_app.delete_payment"
    model = Payment
    template_name = "del_payment_form.html"
    success_url = "/site_moderator/"


# 3 testy
class UserListView(PermissionRequiredMixin, ListView):
    permission_required = "eshopp_app.view_payment"
    model = User
    fields = "groups"
    template_name = "user_list.html"


# 3 testy 2 get 1 post
class EditUserPermissionView(PermissionRequiredMixin, UpdateView):
    permission_required = "eshopp_app.view_payment"
    model = User
    fields = ("groups",)
    template_name = "form.html"
    success_url = "/site_moderator/"


# 3 tests
class AdminView(PermissionRequiredMixin, View):
    permission_required = "eshopp_app.view_payment"

    def get(self, request):
        return render(request, "admin_list_view.html")

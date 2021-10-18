"""djangoeshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from eshopp_app.views import MainMenuView, ProductsListView, CategoriesListView, CategoryDetailsView, \
    ProductDetailsView, CartDetailsView, CreateUser, CartProductCreateView, DelCartProductView, \
    UserProfilView, DeleteUserView, EditUserProfil, OrderDetailView, CreateOrderView, RemoveCartProductView, \
    AddProductView, EditProductView, DeleteProductView, AddCategoryView, EditCategoryView, DeleteCategoryView, \
    SearchResultsView, AddDeliveryView, EditDeliveryView, DeleteDeliveryView, DeliveryListView, DeliveryDetailView, \
    PaymentListView, PaymentDetailView, AddPaymentView, EditPaymentView, DeletePaymentView, AdminView, EditUserData, \
    UserListView, EditUserPermissionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('', MainMenuView.as_view(), name="main-menu"),
    path('', include('django.contrib.auth.urls')),
    path('products/', ProductsListView.as_view(),  name="list_products"),
    path('product/<int:pk>/', ProductDetailsView.as_view(), name="product-detail"),
    path("categories/", CategoriesListView.as_view(), name="categories-list-view"),
    path('category/<int:pk>/', CategoryDetailsView.as_view(), name="category-details"),
    path("cart/", CartDetailsView.as_view(), name="cart-view"),
    path('add_to_cart/<int:pk>/', CartProductCreateView.as_view(), name="add_to_cart"),
    path('register/', CreateUser.as_view(), name="register-view"),
    path('edit_cart/<int:pk>', RemoveCartProductView.as_view(), name="edit-cart-product"),
    path("del_card_prod/<int:pk>/", DelCartProductView.as_view(), name="delete-cart-product"),
    path("profil_details/", UserProfilView.as_view(), name="profil-view"),
    path("del_profil/", DeleteUserView.as_view(), name="delete-user"),
    path("edit_profil/", EditUserProfil.as_view(), name="edit-user"),
    path("edit_user/", EditUserData.as_view(), name="edit-user-info"),
    path("create_order/", CreateOrderView.as_view(), name="create-order"),
    path("order_detail/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("add_product/", AddProductView.as_view(), name="add-product"),
    path("edit_product/<int:pk>/", EditProductView.as_view(), name="edit-product"),
    path("delete_product/<int:pk>/", DeleteProductView.as_view(), name="delete-product"),
    path("add_category/", AddCategoryView.as_view(), name="add-category"),
    path("edit_category/<int:pk>/", EditCategoryView.as_view(), name="edit-category"),
    path("delete_category/<int:pk>/", DeleteCategoryView.as_view(), name="delete-category"),
    path("delivery_list/", DeliveryListView.as_view(), name="delivery-list"),
    path("delivery_details/<int:pk>/", DeliveryDetailView.as_view(), name="delivery-detail"),
    path("add_delivery/", AddDeliveryView.as_view(), name="add-delivery"),
    path("edit_delivery/<int:pk>/", EditDeliveryView.as_view(), name="edit-delivery"),
    path("delete_delivery/<int:pk>/", DeleteDeliveryView.as_view(), name="delete-delivery"),
    path("payment_list/", PaymentListView.as_view(), name="payment-list"),
    path("payment_details/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("add_payment/", AddPaymentView.as_view(), name="add-payment"),
    path("edit_payment/<int:pk>/", EditPaymentView.as_view(), name="edit-payment"),
    path("delete_payment/<int:pk>/", DeletePaymentView.as_view(), name="delete-payment"),
    path("user_list/", UserListView.as_view(), name="user-list"),
    path("add_permission/<int:pk>", EditUserPermissionView.as_view(), name="add-permission"),
    path("site_moderator/", AdminView.as_view(), name="site-moderator"),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

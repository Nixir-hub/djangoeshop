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
    SearchResultsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('', MainMenuView.as_view(), name="main-menu"),
    path('', include('django.contrib.auth.urls')),
    path('products/', ProductsListView.as_view(),  name="list_products"),
    path('product/<int:pk>/', ProductDetailsView.as_view(), name="product-detail"),
    path("categories/", CategoriesListView.as_view(), name="categories-list-view"),
    path('category/<int:pk>/', CategoryDetailsView.as_view(), name="category-details"),
    path("cart", CartDetailsView.as_view(), name="cart-view"),
    path('add_to_cart/<int:pk>/', CartProductCreateView.as_view(), name="add_to_cart"),
    path('register/', CreateUser.as_view(), name="register-view"),
    path('edit_cart/<int:pk>', RemoveCartProductView.as_view(), name="edit-cart-product"),
    path("del_card_prod/<int:pk>/", DelCartProductView.as_view(), name="delete-cart-product"),
    path("profil_details/", UserProfilView.as_view(), name="profil-view"),
    path("del_profil/<int:pk>/", DeleteUserView.as_view(), name="delete-user"),
    path("edit_profil/<int:pk>/", EditUserProfil.as_view(), name="edit-user"),
    path("create_order/", CreateOrderView.as_view(), name="create-order"),
    path("order_detail/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("add_product/", AddProductView.as_view(), name="add-product"),
    path("edit_product/<int:pk>/", EditProductView.as_view(), name="edit-product"),
    path("delete_product/<int:pk>/", DeleteProductView.as_view(), name="delete-product"),
    path("add_category/", AddCategoryView.as_view(), name="add-category"),
    path("edit_category/<int:pk>/", EditCategoryView.as_view(), name="edit-category"),
    path("delete_category/<int:pk>/", DeleteCategoryView.as_view(), name="delete-category")
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

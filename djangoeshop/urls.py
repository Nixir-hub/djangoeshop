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
from django.contrib import admin
from django.urls import path, include

from eshopp_app.views import MainMenuView, ProductsListView, CategoriesListView, CategoryDetailsView, \
    ProductDetailsView, CartDetailsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainMenuView.as_view(), name="main-menu"),
    path('', include('django.contrib.auth.urls')),
    path('products/', ProductsListView.as_view(),  name="list_products"),
    path('product/<int:pk>', ProductDetailsView.as_view(), name="product-detail"),
    path("categories/", CategoriesListView.as_view(), name="categories-list-view"),
    path('category/<int:pk>', CategoryDetailsView.as_view(), name="category-details"),
    path("cart/<int:pk>", CartDetailsView.as_view(), name="cart-view")
]

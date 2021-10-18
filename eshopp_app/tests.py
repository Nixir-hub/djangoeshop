import tempfile
import faker
import pytest
from django.contrib.auth.models import User

from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy

from eshopp_app.models import Category, Product, Profile, Order, Payment, Delivery


def test_get_main_view():
    client = Client()
    response = client.get(reverse("main-menu"))
    assert response.status_code == 200


def test_post_main_view():
    client = Client()
    response = client.post(reverse("main-menu"))
    assert response.status_code == 405


@pytest.mark.django_db
def test_product_list_get_empty():
    client = Client()
    response = client.get(reverse("list_products"))
    assert response.status_code == 200
    products_list = response.context['object_list']
    assert products_list.count() == 0


@pytest.mark.django_db
def test_product_list_get_not_empty(products):
    client = Client()
    response = client.get(reverse("list_products"))
    assert response.status_code == 200
    products_list = response.context['object_list']
    assert products_list.count() == len(products)
    for product in products:
        assert product in products_list


@pytest.mark.django_db
def test_get_product_detail_view(product):
    client = Client()
    response = client.get(reverse("product-detail", args=(product.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_no_product_detail_view():
    client = Client()
    response = client.get(reverse("product-detail", args=(1,)))
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_product_add_no_login():
    client = Client()
    response = client.get(reverse("add-product"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_add_product_login_normal(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("add-product"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_add_product_login_with_permission(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("add-product"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_add_product(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    category = Category.objects.create(name="test", img="photos/furniture.jpeg")
    a ={
        "name": "xsda",
        "description": "xsda",
        "stock": "23",
        "price_netto": "12",
        "categories": category.id,
        "vat": "1",
        "SKU": "10",
    }
    response = client.post(reverse("add-product"), data=a)
    assert response.status_code == 302
    Product.objects.get(**a)


@pytest.mark.django_db
def test_get_product_edit_no_login(product):
    client = Client()
    response = client.get(reverse("edit-product", args=(product.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_edit_product_login_normal(user_normal, product):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("edit-product", args=(product.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_edit_product_login_with_permission(user_with_permissions, product):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("edit-product", args=(product.pk,)))
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_edit_product_post(user_with_permissions, product):
#     client = Client()
#     client.force_login(user_with_permissions)
#     category = Category.objects.create(name="test")
#     category.save()
#     a ={
#         "name": product.name,
#         "description": product.description,
#         "stock": product.stock,
#         "price_netto": product.price_netto,
#         "categories": category,
#         "vat": product.vat,
#         "SKU": product.SKU,
#         "in_stock": product.in_stock,
#         "img": product.img
#     }
#     response = client.post(reverse("edit-product", args=(product.pk,)), data=a)
#     assert response.status_code == 302

@pytest.mark.django_db
def test_get_delete_product_no_login(product):
    client = Client()
    response = client.get(reverse("delete-product", args=(product.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_delete_product_login_normal(user_normal, product):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("delete-category", args=(product.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_del_product_login_with_perm(user_with_permissions, category):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("delete-category", args=(category.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_del_category_post(user_with_permissions, product):
    client = Client()
    client.force_login(user_with_permissions)

    response = client.post(reverse("delete-product", args=(product.pk,)))
    assert response.status_code == 302
    with pytest.raises(Category.DoesNotExist):
        Product.objects.get(id = product.pk)


@pytest.mark.django_db
def test_category_list_get_empty():
    client = Client()
    response = client.get(reverse("categories-list-view"))
    assert response.status_code == 200
    products_list = response.context['object_list']
    assert products_list.count() == 0


@pytest.mark.django_db
def test_category_list_get_not_empty(categories):
    client = Client()
    response = client.get(reverse("categories-list-view"))
    assert response.status_code == 200
    categories_list = response.context['object_list']
    assert categories_list.count() == len(categories)
    for product in categories:
        assert product in categories_list


@pytest.mark.django_db
def test_get_category_detail_view(category):
    client = Client()
    response = client.get(reverse("category-details", args=(category.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_category_detail_view_empty():
    client = Client()
    response = client.get(reverse("category-details", args=(1,)))
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_add_category_login_normal(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("add-category"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_add_category_login_with_permission(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("add-category"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_category_post(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    a ={
        "name": "testCategory",
    }
    response = client.post(reverse("add-category"), data=a)
    assert response.status_code == 302
    Category.objects.get(**a)


@pytest.mark.django_db
def test_get_category_edit_no_login(category):
    client = Client()
    response = client.get(reverse("edit-category", args=(category.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_edit_category_login_normal(user_normal, category):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("edit-category", args=(category.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_edit_category_login_with_perm(user_with_permissions, category):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("edit-category", args=(category.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_category_post(user_with_permissions, category):
    client = Client()
    client.force_login(user_with_permissions)
    a ={
        "name": "testCategory",
    }
    response = client.post(reverse("edit-category", args=(category.pk,)), data=a)
    assert response.status_code == 302
    assert Category.objects.get(**a).name == "testCategory"


@pytest.mark.django_db
def test_get_delete_category_no_login(category):
    client = Client()
    response = client.get(reverse("delete-category", args=(category.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_delete_category_login_normal(user_normal, category):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("delete-category", args=(category.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_del_category_login_with_perm(user_with_permissions, category):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("edit-category", args=(category.pk,)))
    assert response.status_code == 200

# Czy tyle wystarczy?
@pytest.mark.django_db
def test_del_category_post(user_with_permissions, category):
    client = Client()
    client.force_login(user_with_permissions)

    response = client.post(reverse("delete-category", args=(category.pk,)))
    assert response.status_code == 302
    with pytest.raises(Category.DoesNotExist):
        Category.objects.get(id = category.pk)


@pytest.mark.django_db
def test_get_cart_details_no_login():
    client = Client()
    response = client.get(reverse("cart-view"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_cart_view_login_normal(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("cart-view"))
    assert response.status_code == 200

## TODO: DO POPRAWY
# @pytest.mark.django_db
# def test_get_delete_cart_product_no_login(cart_product):
#     client = Client()
#     response = client.get(reverse("delete-cart-product", args=(cart_product.pk,)))
#     assert response.status_code == 302


@pytest.mark.django_db
def test_get_delete_cart_product_login_normal(user_normal, cart_product):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("delete-cart-product", args=(cart_product.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_profil_detail_view_logged(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("profil-view"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_profil_detail_view_no_login():
    client = Client()
    response = client.get(reverse("profil-view"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_profil_delete_view_no_login():
    client = Client()
    response = client.get(reverse("delete-user"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_profil_delete_view_login(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("delete-user"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_del_user_post(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.post(reverse("delete-user"))
    assert response.status_code == 302
    with pytest.raises(User.DoesNotExist):
        User.objects.get(id=user_normal.pk)


@pytest.mark.django_db
def test_get_user_change_pass_view_login(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse('password_change'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_user_change_pass_view_no_login():
    client = Client()
    response = client.get(reverse('password_change'))
    assert response.status_code == 302


@pytest.mark.django_db
def test_change_password_post(user_normal):
    client = Client()
    client.force_login(user_normal)
    a ={
        "old_password": "password1",
        "new_password1": "testhasla1",
        "new_password2": "testhasla1"
    }
    response = client.post(reverse("password_change"), data=a)
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_edit_user_no_login():
    client = Client()
    response = client.get(reverse("edit-user-info"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_edit_user_login_normal(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("edit-user-info"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_user_f_l_name_post(user_normal):
    client = Client()
    client.force_login(user_normal)
    a = {
        "first_name": "newname",
        "last_name": "newlastname"
    }
    response = client.post(reverse("edit-user-info"), data=a)
    assert response.status_code == 302
    assert User.objects.get(id= user_normal.pk).first_name == "newname"


@pytest.mark.django_db
def test_get_edit_user_adres_no_login():
    client = Client()
    response = client.get(reverse("edit-user"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_edit_user_adres_login_normal(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("edit-user"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_user_adres_post(user_normal):
    client = Client()
    client.force_login(user_normal)
    a = {
        "adres": "newadres",
        "phone": "60"
    }
    response = client.post(reverse("edit-user"), data=a)
    assert response.status_code == 302
    assert Profile.objects.get(user=user_normal).adres == "newadres"


@pytest.mark.django_db
def test_get_order_detail_view_login(user_normal, order):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("order-detail", args=(order.id,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_order_detail_view_login_other_user(user_normal_2, order):
    client = Client()
    client.force_login(user_normal_2)
    response = client.get(reverse("order-detail", args=(order.id,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_delivery_list_view_no_permission(user_normal, delivery_method_list):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("delivery-list"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_delivery_list_view_user_with_permission(user_with_permissions, delivery_method_list):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("delivery-list"))
    assert response.status_code == 200
    delivery_list = response.context['object_list']
    assert delivery_list.count() == len(delivery_method_list)
    for delivery in delivery_method_list:
        assert delivery in delivery_list



@pytest.mark.django_db
def test_product_list_get_empty(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("list_products"))
    assert response.status_code == 200
    products_list = response.context['object_list']
    assert products_list.count() == 0


@pytest.mark.django_db
def test_get_product_detail_view_no_login(delivery_method):
    client = Client()
    response = client.get(reverse("delivery-detail", args=(delivery_method.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_no_product_detail_view(user_normal, delivery_method):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("delivery-detail", args=(delivery_method.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_no_product_detail_view(user_with_permissions, delivery_method):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("delivery-detail", args=(delivery_method.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_delivery_add_no_login():
    client = Client()
    response = client.get(reverse("add-delivery"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_add_delivery_login_normal(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("add-delivery"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_add_delivery_login_with_permission(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("add-delivery"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_add_delivery(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    a ={
        "name": "testdelivery",
        "delivery_method": "1"
    }
    response = client.post(reverse("add-delivery"), data=a)
    assert response.status_code == 302
    assert Delivery.objects.get(**a).name == "testdelivery"


@pytest.mark.django_db
def test_get_delivery_edit_no_login(delivery_method):
    client = Client()
    response = client.get(reverse("edit-delivery", args=(delivery_method.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_edit_delivery_login_normal(user_normal, delivery_method):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("edit-delivery", args=(delivery_method.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_edit_delivery_login_with_permission(user_with_permissions, delivery_method):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("edit-delivery", args=(delivery_method.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_delivery_post(user_with_permissions, delivery_method):
    client = Client()
    client.force_login(user_with_permissions)
    category = Category.objects.create(name="test")
    category.save()
    a ={
        "name": "newdeliveryname",
        "delivery_method": delivery_method.delivery_method

    }
    response = client.post(reverse("edit-delivery", args=(delivery_method.pk,)), data=a)
    assert response.status_code == 302
    assert Delivery.objects.get(id=delivery_method.pk).name == "newdeliveryname"


@pytest.mark.django_db
def test_get_delivery_delete_view_no_login(delivery_method):
    client = Client()
    response = client.get(reverse("delete-delivery", args=(delivery_method.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_delivery_delete_view_login(user_normal, delivery_method):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("delete-delivery", args=(delivery_method.pk,)))
    assert response.status_code == 403

@pytest.mark.django_db
def test_get_delivery_delete_view_login(user_with_permissions, delivery_method):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("delete-delivery", args=(delivery_method.pk,)))
    assert response.status_code == 200

@pytest.mark.django_db
def test_del_delivery_post(user_with_permissions, delivery_method):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.post(reverse("delete-delivery", args=(delivery_method.pk,)))
    assert response.status_code == 302
    with pytest.raises(Delivery.DoesNotExist):
        Delivery.objects.get(id=delivery_method.pk)
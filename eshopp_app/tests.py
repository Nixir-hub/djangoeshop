import pytest
from django.contrib.auth.models import User, Group
from django.test import Client
from django.urls import reverse
from eshopp_app.models import Category, Product, Profile, Order, Payment, Delivery, CartProduct


@pytest.mark.django_db
def test_get_main_view_with_products_no_login(products):
    client = Client()
    response = client.get(reverse("main-menu"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_main_view_login_without_products(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("main-menu"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_main_view_login(user_normal, products):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("main-menu"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_main_view_with_products_no_login(products):
    client = Client()
    response = client.post(reverse("main-menu"))
    assert response.status_code == 405


@pytest.mark.django_db
def test_post_main_view_login_without_products(user_normal):
    client = Client()
    client.force_login(user_normal)
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
    a = {
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
def test_post_add_product_no_login():
    client = Client()
    category = Category.objects.create(name="test", img="photos/furniture.jpeg")
    a = {
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
    with pytest.raises(Product.DoesNotExist):
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


@pytest.mark.django_db
def test_edit_product_post(user_with_permissions, product, category):
    client = Client()
    client.force_login(user_with_permissions)
    a ={
        "name": "test",
        "description": "testdescripiton",
        "stock": "100",
        "price_netto": "1000",
        "categories": category.id,
        "vat": "1",
        "SKU": "100",
        "in_stock": "True",
    }
    response = client.post(reverse("edit-product", args=(product.pk,)), data=a)
    assert response.status_code == 302
    assert Product.objects.get(id=product.pk).name == "test"
    assert Product.objects.get(id=product.pk).description == "testdescripiton"


@pytest.mark.django_db
def test_get_delete_product_no_login(product):
    client = Client()
    response = client.get(reverse("delete-product", args=(product.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_delete_product_login_normal(user_normal, product):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("delete-product", args=(product.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_del_product_login_with_perm(user_with_permissions, product):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("delete-product", args=(product.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_del_product_post_login_user_with_permission(user_with_permissions, product):
    client = Client()
    client.force_login(user_with_permissions)

    response = client.post(reverse("delete-product", args=(product.pk,)))
    assert response.status_code == 302
    with pytest.raises(Product.DoesNotExist):
        Product.objects.get(id=product.pk)


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
    a = {
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
    a = {
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


@pytest.mark.django_db
def test_del_category_post(user_with_permissions, category):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.post(reverse("delete-category", args=(category.pk,)))
    assert response.status_code == 302
    with pytest.raises(Category.DoesNotExist):
        Category.objects.get(id=category.pk)


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
    a = {
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
    assert User.objects.get(id=user_normal.pk).first_name == "newname"


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
        "company_adres": "-",
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
    response = client.get(reverse("order-detail", args=(order.pk,)))
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
def test_delivery_list_get_empty(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("delivery-list"))
    assert response.status_code == 200
    products_list = response.context['object_list']
    assert products_list.count() == 0


@pytest.mark.django_db
def test_get_delivery_detail_view_no_login(delivery_method):
    client = Client()
    response = client.get(reverse("delivery-detail", args=(delivery_method.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_no_delivery_detail_view(user_normal, delivery_method):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("delivery-detail", args=(delivery_method.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_no_delivery_detail_view(user_with_permissions, delivery_method):
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
    a = {
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
    a = {
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


@pytest.mark.django_db
def test_get_payment_list_view_no_permission(user_normal, payments):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("payment-list"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_payment_list_view_user_with_permission(user_with_permissions, payments):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("payment-list"))
    assert response.status_code == 200
    payment_list = response.context['object_list']
    assert payment_list.count() == len(payments)
    for payment in payments:
        assert payment in payments


@pytest.mark.django_db
def test_payment_list_get_empty(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("payment-list"))
    assert response.status_code == 200
    products_list = response.context['object_list']
    assert products_list.count() == 0


@pytest.mark.django_db
def test_get_payment_detail_view_no_login(payment):
    client = Client()
    response = client.get(reverse("payment-detail", args=(payment.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_no_payment_detail_view(user_normal, payment):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("payment-detail", args=(payment.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_no_payment_detail_view(user_with_permissions, payment):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("payment-detail", args=(payment.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_payment_add_no_login():
    client = Client()
    response = client.get(reverse("add-payment"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_add_payment_login_normal(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("add-payment"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_add_payment_login_with_permission(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("add-payment"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_add_payment(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    a = {
        "name": "testpayment",
    }
    response = client.post(reverse("add-payment"), data=a)
    assert response.status_code == 302
    assert Payment.objects.get(**a).name == "testpayment"


@pytest.mark.django_db
def test_get_payment_edit_no_login(payment):
    client = Client()
    response = client.get(reverse("edit-payment", args=(payment.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_edit_payment_login_normal(user_normal, payment):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("edit-payment", args=(payment.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_edit_payment_login_with_permission(user_with_permissions, payment):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("edit-payment", args=(payment.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_payment_post(user_with_permissions, payment):
    client = Client()
    client.force_login(user_with_permissions)
    a = {
        "name": "newpayment",
        "id_done": payment.is_done

    }
    response = client.post(reverse("edit-payment", args=(payment.pk,)), data=a)
    assert response.status_code == 302
    assert Payment.objects.get(id=payment.pk).name == "newpayment"


@pytest.mark.django_db
def test_get_payment_delete_view_no_login(payment):
    client = Client()
    response = client.get(reverse("delete-payment", args=(payment.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_payment_delete_view_login(user_normal, payment):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("delete-payment", args=(payment.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_payment_delete_view_login(user_with_permissions, payment):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("delete-payment", args=(payment.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_del_payment_post(user_with_permissions, payment):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.post(reverse("delete-payment", args=(payment.pk,)))
    assert response.status_code == 302
    with pytest.raises(Payment.DoesNotExist):
        Payment.objects.get(id=payment.pk)


@pytest.mark.django_db
def test_get_user_list_view_no_permission(user_normal, users):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("user-list"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_payment_list_view_user_with_permission(user_with_permissions, users):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("user-list"))
    assert response.status_code == 200
    payment_list = response.context['object_list']
    assert payment_list.count()-1 == len(users)
    for payment in users:
        assert payment in users


@pytest.mark.django_db
def test_payment_list_get_empty(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("user-list"))
    assert response.status_code == 200
    products_list = response.context['object_list']
    assert products_list.count() == 1


@pytest.mark.django_db
def test_get_user_edit_no_login(user_normal):
    client = Client()
    response = client.get(reverse("add-permission", args=(user_normal.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_edit_user_login_normal(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("add-permission", args=(user_normal.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_edit_user_login_with_permission(user_with_permissions, user_normal):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("add-permission", args=(user_normal.pk,)))
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_payment_post(user_with_permissions, user_normal):
    client = Client()
    client.force_login(user_with_permissions)
    group = Group.objects.create(name="x")
    a = {
        "groups": group.id,
    }
    response = client.post(reverse("add-permission", args=(user_normal.pk,)), data=a)
    assert response.status_code == 302
    assert user_normal.groups.all()[0].name == group.name


@pytest.mark.django_db
def test_get_admin_detail_view_no_login():
    client = Client()
    response = client.get(reverse("site-moderator"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_admin_detail_view_login_no_perm(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("site-moderator"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_admin_detail_view(user_with_permissions):
    client = Client()
    client.force_login(user_with_permissions)
    response = client.get(reverse("site-moderator"))
    assert response.status_code == 200


# # Czy tak testować?
# @pytest.mark.django_db
# def test_get_payment_delete_view_no_login(cart_product):
#     client = Client()
#     response = client.get(reverse("delete-cart-product", args=(cart_product.pk,)))
#     assert response.status_code == 302
#     assert pytest.raises(AttributeError)


@pytest.mark.django_db
def test_get_payment_delete_view_login_other_user(user_normal_2, cart_product):
    client = Client()
    client.force_login(user_normal_2)
    response = client.get(reverse("delete-cart-product", args=(cart_product.pk,)))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_cart_product_delete_view_login(user_normal, cart_product):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("delete-cart-product", args=(cart_product.pk,)))
    assert response.status_code == 302
    with pytest.raises(CartProduct.DoesNotExist):
        user_normal.cart.cartproduct_set.get(id=cart_product.id)


@pytest.mark.django_db
def test_get_add_product_to_cart_delete_view_no_login(product):
    client = Client()
    response = client.get(reverse("add_to_cart", args=(product.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_add_product_to_cart_view_login_cp_quantity_same_as_product_stock(user_normal, cart_product, product):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("add_to_cart", args=(product.pk,)))
    assert response.status_code == 200
    assert user_normal.cart.cartproduct_set.get(product=product).quantity == product.stock


@pytest.mark.django_db
def test_get_add_product_to_cart_view_login_cartproduct_quantity0(user_normal, product):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("add_to_cart", args=(product.pk,)))
    assert response.status_code == 302
    assert user_normal.cart.cartproduct_set.get(product=product).quantity == 1


@pytest.mark.django_db
def test_get_remove_product_to_cart_delete_view_no_login(product):
    client = Client()
    response = client.get(reverse("edit-cart-product", args=(product.pk,)))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_remove_product_to_cart_view_login_cart_product_quantity_2(user_normal, cart_product_quantity_2, product):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("edit-cart-product", args=(product.pk,)))
    assert response.status_code == 302
    assert user_normal.cart.cartproduct_set.get(id=cart_product_quantity_2.id).quantity == 1


@pytest.mark.django_db
def test_get_remove_product_to_cart_view_login_cart_product_quantity_1(user_normal, cart_product, product):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("edit-cart-product", args=(product.pk,)))
    assert response.status_code == 302
    with pytest.raises(CartProduct.DoesNotExist):
        user_normal.cart.cartproduct_set.get(id=cart_product.id)


@pytest.mark.django_db
def test_get_order_create_no_login():
    client = Client()
    response = client.get(reverse("create-order"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_create_order_with_cart_product_login_normal(user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.get(reverse("create-order"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_create_order_with_cart_product_login_normal(user_normal_2):
    client = Client()
    client.force_login(user_normal_2)
    response = client.get(reverse("create-order"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_add_delivery_login_normal(user_normal):
    client = Client()
    client.force_login(user_normal)

    response = client.get(reverse("create-order"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_register_user():
    client = Client()
    response = client.post(reverse("register-view"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_register_user():
    client = Client()
    a = {
        "username": "testcreateuser11",
        "first_name": "testname",
        "last_name": "testsurname",
        "email": "test@email.com",
        "password1": "testpassword1",
        "password2": "testpassword1"
    }
    response = client.post(reverse("register-view"), data=a)
    assert response.status_code == 302
    assert User.objects.get(username="testcreateuser11").profile
    assert User.objects.get(username="testcreateuser11").cart
    assert User.objects.get(username="testcreateuser11").discount_set.all()


@pytest.mark.django_db
def test_get_crate_order_no_login_user():
    client = Client()
    response = client.post(reverse("create-order"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_crate_order_login_user_with_cart_product(product, cart_product, user_normal):
    client = Client()
    client.force_login(user_normal)
    response = client.post(reverse("create-order"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_get_crate_order_login_user_no_cart_product(user_normal_2):
    client = Client()
    client.force_login(user_normal_2)
    response = client.post(reverse("create-order"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_post_crate_order_login_user_with_cart_product(cart_product, order, user_normal):
    client = Client()
    client.force_login(user_normal)
    assert len(user_normal.cart.cartproduct_set.all()) != 0
    a = {
        "payment": order.payment.id,
        "delivery_method": order.delivery_method.id
    }
    response = client.post(reverse("create-order"), data=a)
    assert response.status_code == 302
    assert len(user_normal.cart.cartproduct_set.all()) == 0
    assert len(Order.objects.filter(user=user_normal)) == 2


@pytest.mark.django_db
def test_post_crate_order_login_user_with_no_cart_product(delivery_method, payment, user_normal_2):
    client = Client()
    client.force_login(user_normal_2)
    assert len(user_normal_2.cart.cartproduct_set.all()) == 0
    assert user_normal_2.discount_set.first().is_active is False
    a = {
        "payment": payment,
        "delivery_method": delivery_method
    }
    response = client.post(reverse("create-order"), data=a)
    assert response.status_code == 302
    assert len(user_normal_2.order_set.all()) == 0


@pytest.mark.django_db
def test_post_crate_order_login_user_with_cart_product_with_discount(cart_product, order, user_normal):
    client = Client()
    client.force_login(user_normal)
    assert len(user_normal.cart.cartproduct_set.all()) != 0
    assert user_normal.discount_set.first().is_active is True
    a = {
        "payment": order.payment.id,
        "delivery_method": order.delivery_method.id
    }
    response = client.post(reverse("create-order"), data=a)
    assert response.status_code == 302
    assert len(user_normal.cart.cartproduct_set.all()) == 0
    assert len(Order.objects.filter(user=user_normal)) == 2
    assert user_normal.discount_set.first().is_active is False


@pytest.mark.django_db
def test_search_list_get_empty():
    client = Client()
    a = {
        "q": "test"
    }
    response = client.get(reverse('search_results'), data=a)
    assert response.status_code == 200
    products_list = response.context['object_list']
    assert products_list.count() == 0


@pytest.mark.django_db
def test_search_list_get_not_empty(product):
    client = Client()
    a = {
        "q": "x"
    }
    response = client.get(reverse('search_results'), data=a)
    products_list = response.context['object_list']
    assert products_list.count() == 1

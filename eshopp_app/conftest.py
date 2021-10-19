import pytest
from django.contrib.auth.models import User, Permission
from eshopp_app.models import Product, Category, Discount, Cart, Profile, CartProduct, Payment, Delivery, Order


@pytest.fixture
def user_normal():
    user = User.objects.create(username="testusername",
                               first_name="testfirst_name",
                               last_name="last_name",
                               email="email")
    user.set_password("password1")
    user.save()
    discount = Discount.objects.create(user=User.objects.get(id=user.id), amount=0.3)
    discount.save()
    cart = Cart.objects.create(user=User.objects.get(id=user.id),
                        discount=Discount.objects.get(user=User.objects.get(id=user.id)))

    cart.save()
    profile = Profile.objects.create(user=User.objects.get(id=user.id), adres="xxx", phone=1112)
    profile.save()
    return user


@pytest.fixture
def user_normal_2():
    user = User.objects.create(username="testusername2",
                               first_name="testfirst_name2",
                               last_name="last_name2",
                               email="email")
    user.set_password("password2")
    user.save()

    discount = Discount.objects.create(user=User.objects.get(id=user.id), amount=0.3)
    discount.save()
    cart = Cart.objects.create(user=User.objects.get(id=user.id),
                               discount=Discount.objects.get(user=User.objects.get(id=user.id)))
    cart.save()
    profile = Profile.objects.create(user=User.objects.get(id=user.id), adres="xxx", phone=1112)
    profile.save()
    return user


@pytest.fixture
def products():
    lst = []
    for x in range(3):
        lst.append(Product.objects.create(name=x, description=x, stock=x, price_netto=x, vat=x, SKU=x, in_stock=True,
                                          img="chair.jpeg"))
    return lst


@pytest.fixture
def user_with_permissions():
    u = User.objects.create(username="testUserWithPermission")
    p = Permission.objects.get(codename="add_product")
    p1 = Permission.objects.get(codename="change_product")
    p2 = Permission.objects.get(codename="add_category")
    p3 = Permission.objects.get(codename="change_category")
    p4 = Permission.objects.get(codename="delete_category")
    p5 = Permission.objects.get(codename="view_delivery")
    p6 = Permission.objects.get(codename="add_delivery")
    p7 = Permission.objects.get(codename="change_delivery")
    p8 = Permission.objects.get(codename="delete_delivery")
    p9 = Permission.objects.get(codename="view_payment")
    p10 = Permission.objects.get(codename="add_payment")
    p11 = Permission.objects.get(codename="change_payment")
    p12 = Permission.objects.get(codename="delete_payment")
    u.user_permissions.add(p)
    u.user_permissions.add(p1)
    u.user_permissions.add(p2)
    u.user_permissions.add(p3)
    u.user_permissions.add(p4)
    u.user_permissions.add(p5)
    u.user_permissions.add(p6)
    u.user_permissions.add(p7)
    u.user_permissions.add(p8)
    u.user_permissions.add(p9)
    u.user_permissions.add(p10)
    u.user_permissions.add(p11)
    u.user_permissions.add(p12)
    return u


@pytest.fixture
def user():
    u = User.objects.create(username="normal_guy")
    return u


@pytest.fixture
def categories():
    lst = []
    for x in range(3):
        lst.append(Category.objects.create(name=x, img="photos/furniture.jpeg"))
    return lst


@pytest.fixture
def category():
    category = Category.objects.create(name="test", img="photos/furniture.jpeg")
    return category


@pytest.fixture
def cart_product(user_normal, product):
    cart_product = CartProduct.objects.create(cart=user_normal.cart, product=product, quantity=1)
    cart_product.save()
    return cart_product


@pytest.fixture
def cart_product_quantity_2(user_normal, product):
    cart_product = CartProduct.objects.create(cart=user_normal.cart, product=product, quantity=2)
    cart_product.save()
    return cart_product


@pytest.fixture
def product(category):
    product = Product.objects.create(name="x", description="x", stock=1, price_netto=1, vat=0.23, SKU=1, in_stock=True,
                                     img="photos/chair.jpeg")
    product.save()
    return product


@pytest.fixture
def payment():
    payment = Payment.objects.create(name="test_payment")
    payment.save()
    return payment


@pytest.fixture
def payments():
    lst = []
    for x in range(5):
        lst.append(Payment.objects.create(name="test_payment"))
    return lst


@pytest.fixture
def delivery_method():
    delivery_method = Delivery.objects.create(name="testdelivery")
    delivery_method.save()
    return delivery_method


@pytest.fixture
def delivery_method_list():
    lst = []
    for x in range(5):
        lst.append(Delivery.objects.create(name="testdelivery"))
    return lst


@pytest.fixture
def order(payment, delivery_method, user_normal):
    order = Order.objects.create(payment=payment, order=1, delivery_method=delivery_method, user=user_normal, price=100)
    order.save()
    return order


@pytest.fixture
def users():
    lst = []
    for x in range(5):
        lst.append(User.objects.create(username=x,
                               first_name=x,
                               last_name=x,
                               email=x))
    return lst
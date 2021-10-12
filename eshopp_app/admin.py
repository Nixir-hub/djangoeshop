from django.contrib import admin

from eshopp_app.models import Product, Category, Cart, Payment, Delivery, Order, Discount

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Payment)
admin.site.register(Delivery)
admin.site.register(Order)
admin.site.register(Discount)

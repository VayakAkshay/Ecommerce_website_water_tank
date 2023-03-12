from django.contrib import admin
from .models import ProductData,CartData,ContactData,ReviewData,WishlistData,OrderItem

admin.site.register(ProductData)
admin.site.register(CartData)
admin.site.register(ContactData)
admin.site.register(ReviewData)
admin.site.register(WishlistData)
admin.site.register(OrderItem)
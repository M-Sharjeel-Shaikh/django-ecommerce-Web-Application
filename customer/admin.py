from django.contrib import admin
from customer.models import Customer, Cart, Ordered, Favourite

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display=('user',)

admin.site.register(Customer,CustomerAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display=('user','product', 'quantity', 'created_at')

admin.site.register(Cart,CartAdmin)


class OrderedAdmin(admin.ModelAdmin):
    list_display=('user','created_at')

admin.site.register(Ordered,OrderedAdmin)


class FavouriteAdmin(admin.ModelAdmin):
    list_display=('user','favourite')

admin.site.register(Favourite,FavouriteAdmin)






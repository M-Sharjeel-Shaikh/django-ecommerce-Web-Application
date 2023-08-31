from django.contrib import admin
from .models import *

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display=('name','seller','category','price', 'discount_price')

admin.site.register(Product,ProductAdmin)



class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name', 'price']

    model = ColorVariant

admin.site.register(ColorVariant ,ColorVariantAdmin)



@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price']

    model = SizeVariant


class SellerAdmin(admin.ModelAdmin):
    list_display=('name',)

admin.site.register(Seller,SellerAdmin)


class CouponAdmin(admin.ModelAdmin):
    list_display=('code','value','expire')

admin.site.register(Coupon,CouponAdmin)


@admin.register(Review)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['product' , 'rate']

    model = Review

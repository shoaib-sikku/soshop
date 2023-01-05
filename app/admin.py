from django.contrib import admin
from .models import (Customer,Product,Cart,OrderPlaced)
# Register your models here.

class CustomerModelAdmin(admin.ModelAdmin):
    list_display= ('id','user','name','locality','city','zipcode')
admin.site.register(Customer,CustomerModelAdmin)


class ProductModelAdmin(admin.ModelAdmin):
    list_display= ('id','title','selling_price','discounted_price','description','brand','category','product_image','slug')
admin.site.register(Product,ProductModelAdmin)


class CartModelAdmin(admin.ModelAdmin):
    list_display= ('id','user','product','quantity',)
admin.site.register(Cart,CartModelAdmin)


class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display= ('id','user','customer','product','quantity','ordered_date','status')
admin.site.register(OrderPlaced,OrderPlacedModelAdmin)

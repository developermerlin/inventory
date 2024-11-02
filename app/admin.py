from django.contrib import admin # type: ignore
from .models import Category,Product,Customer,Supplier,Purchase,TemporaryCart,FinalCart
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Purchase)
admin.site.register(TemporaryCart)
admin.site.register(FinalCart)
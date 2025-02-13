from django.contrib import admin
from .models import ProductCategory, Product,ProductVariant, ProductImage, SupplierList,Supplier # Import models

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(SupplierList)
admin.site.register(Supplier)
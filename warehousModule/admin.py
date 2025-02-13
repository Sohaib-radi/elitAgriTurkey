from django.contrib import admin
from .models import Warehouse, WarehouseProduct,QuantityControl, QuantityReminder
admin.site.register(Warehouse)
admin.site.register(WarehouseProduct)
admin.site.register(QuantityControl)
admin.site.register(QuantityReminder)

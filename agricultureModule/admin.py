from django.contrib import admin
from .models import Land, Region, Product,LandCondition, Statistics, Crop # Import models

admin.site.register(Land)
admin.site.register(Region)
admin.site.register(Product)
admin.site.register(LandCondition)
admin.site.register(Statistics)
admin.site.register(Crop)
from django.contrib import admin
from .models import Wilaya, Land,LandDocument, LandImage, LandTransaction

admin.site.register(Wilaya)
admin.site.register(Land)
admin.site.register(LandDocument)
admin.site.register(LandImage)
admin.site.register(LandTransaction)

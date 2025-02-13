from django.db import models
from django.utils.translation import gettext_lazy as _



#TODO : THIS MODULE WILL BE USED TO MANAGE THE AGRICULTURAL LAND AND THE ENTIRE PROCCESS, IT WILL BE USER TO HAVE4
#       A VISIBILITY ON ANY OF THE AGRICULTURAL LANDS IN THE SYSTEM

# Enum choices
class LandConditionChoices(models.TextChoices):
    PLOWING = "PLOWING", str(_("Plowing"))  # حراثة
    SMOOTHING = "SMOOTHING", str(_("Smoothing"))  # تنعيم
    PLANTING = "PLANTING", str(_("Planting"))  # زراعة
    NON_ARABLE = "NON_ARABLE", str(_("Non-arable"))  # غير قابلة للزراعة
    TREATMENT = "TREATMENT", str(_("Treatment"))  # علاج
    UNUSED = "UNUSED", str(_("Unused"))  # غير مستخدمة

class CropUsageChoices(models.TextChoices):
    SALE = "SALE", str(_("Sale"))  # للبيع
    ANIMAL_FEED = "ANIMAL_FEED", str(_("Animal Feed"))  # كعلف للحيوانات

class ActiveManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Region Name"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    
    objects = ActiveManager()
    
    def __str__(self):
        return self.name

class Land(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="lands", verbose_name=_("Region"))
    land_id = models.CharField(max_length=20, unique=True, verbose_name=_("Land Identifier"))
    name = models.CharField(max_length=255, verbose_name=_("Land Name"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    
    objects = ActiveManager()
    
    def __str__(self):
        return f"{self.name} ({self.land_id})"

class Product(models.Model):
    CATEGORY_CHOICES = [("Seed", _("بذور")), ("Fertilizer", _("سماد"))]
    
    name = models.CharField(max_length=255, verbose_name=_("Product Name"))
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, verbose_name=_("Category"))
    manufacturer = models.CharField(max_length=255, verbose_name=_("Manufacturer"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    
    objects = ActiveManager()
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class LandCondition(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name="conditions", verbose_name=_("Land"))
    condition = models.CharField(max_length=50, choices=LandConditionChoices.choices, verbose_name=_("Condition"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    #TODO : A PRODUCT MUST BE LINKED WIDTH PRODUCT MODELE
    product_used = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="used_in_conditions", verbose_name=_("Product Used"))
    quantity_used = models.FloatField(blank=True, null=True, verbose_name=_("Quantity Used"))
    date = models.DateField(auto_now_add=True, verbose_name=_("Date"))
    
    objects = models.Manager()
    
    def __str__(self):
        return f"{self.land.name} - {self.condition} ({self.date})"

class Crop(models.Model):
    STATUS_CHOICES = [("Planted", _("تم الزراعة")), ("Growing", _("ينمو")), ("Harvested", _("تم الحصاد"))]
    
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name="crops", verbose_name=_("Land"))
    crop_id = models.CharField(max_length=20, unique=True, verbose_name=_("Crop Identifier"))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name=_("Status"))
    quantity = models.FloatField(verbose_name=_("Quantity"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    harvest_date = models.DateField(null=True, blank=True, verbose_name=_("Harvest Date"))
    usage = models.CharField(max_length=50, choices=CropUsageChoices.choices, verbose_name=_("Usage"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    
    objects = ActiveManager()
    
    def __str__(self):
        return f"{self.crop_id} - {self.status} ({self.land.name})"

class Statistics(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="statistics", verbose_name=_("Region"))
    total_land = models.IntegerField(verbose_name=_("Total Land"))
    total_crops = models.IntegerField(verbose_name=_("Total Crops"))
    total_yield = models.FloatField(verbose_name=_("Total Yield (tons)"))
    report_date = models.DateField(auto_now_add=True, verbose_name=_("Report Date"))
    
    def __str__(self):
        return f"Stats for {self.region.name} ({self.report_date})"

    @staticmethod
    def generate_statistics():
        from django.db.models import Sum, Count
        
        stats = []
        for region in Region.objects.all():
            total_land = region.lands.count()
            total_crops = Crop.objects.filter(land__region=region).count()
            total_yield = Crop.objects.filter(land__region=region).aggregate(Sum("quantity"))["quantity__sum"] or 0
            
            stats.append(Statistics.objects.create(
                region=region,
                total_land=total_land,
                total_crops=total_crops,
                total_yield=total_yield,
            ))
        return stats

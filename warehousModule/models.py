from django.db import models
from django.utils.translation import gettext_lazy as _
from productModule.models import Product  


class CustomFieldQuerySet(models.QuerySet):
    def custom_filter(self, **kwargs): return self.filter(**kwargs)  

class CustomFieldManager(models.Manager):
    def get_queryset(self): return CustomFieldQuerySet(self.model, using=self._db)
    def custom_filter(self, **kwargs): return self.get_queryset().custom_filter(**kwargs)


class Warehouse(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Warehouse Name"), help_text=_("Name of the warehouse"))  # الاسم
    image = models.ImageField(upload_to='warehouses/', null=True, blank=True, verbose_name=_("Image"), help_text=_("Attach an image for the warehouse"))  # إرفاق صورة
    description = models.TextField(verbose_name=_("Description"), help_text=_("Warehouse description"))  # الوصف
    space = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Space"), help_text=_("Total available space"))  # المساحة
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the warehouse was added"))  # تاريخ الإنشاء

    objects = CustomFieldManager()  

    def __str__(self): return self.name
    class Meta:
        verbose_name = _("Warehouse") 
        verbose_name_plural = _("Warehouses")  
        ordering = ['name']  


class WarehouseProduct(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='warehouse_products', verbose_name=_("Warehouse"), help_text=_("Associated warehouse"))  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='warehouse_entries', verbose_name=_("Product"), help_text=_("Product added to warehouse"))   
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"), help_text=_("Quantity added to the warehouse")) 
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Weight"), help_text=_("Weight of the added product")) 
    used_space = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Used Space"), help_text=_("Space occupied in the warehouse")) 
    date = models.DateField(verbose_name=_("Date"), help_text=_("Date when the product was added"))  

    objects = CustomFieldManager()  

    def __str__(self): return f"{self.product} in {self.warehouse}"
    class Meta:
        verbose_name = _("Warehouse Product Entry") 
        verbose_name_plural = _("Warehouse Product Entries") 
        ordering = ['-date']  


class QuantityControl(models.Model):
    GOAL_CHOICES = [  
        ('INC', _("Increase")),  
        ('DEC', _("Decrease")),  
    ]
    TIME_FRAME_CHOICES = [  
        ('1D', _("One Day")),      
        ('2D', _("Two Days")),    
        ('3D', _("Three Days")),  
        ('1W', _("One Week")),     
        ('1M', _("One Month")), 
        ('1Y', _("One Year")),     
    ]
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='quantity_controls', verbose_name=_("Warehouse"), help_text=_("Warehouse for quantity control"))  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='quantity_controls', verbose_name=_("Product"), help_text=_("Product for quantity control"))  
    goal = models.CharField(max_length=3, choices=GOAL_CHOICES, verbose_name=_("Goal"), help_text=_("Target: Increase or Decrease quantity"))  
    time_frame = models.CharField(max_length=2, choices=TIME_FRAME_CHOICES, verbose_name=_("Time Frame"), help_text=_("Time period for adjustment"))  
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Quantity"), help_text=_("Quantity adjustment amount based on selected time"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the control was set")) 

    objects = CustomFieldManager()  

    def __str__(self): return f"{self.get_goal_display()} {self.quantity} of {self.product} in {self.warehouse}"
    class Meta:
        verbose_name = _("Quantity Control") 
        verbose_name_plural = _("Quantity Controls")  
        ordering = ['-created_at']  


class QuantityReminder(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='quantity_reminders', verbose_name=_("Warehouse"), help_text=_("Warehouse for reminder"))  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='quantity_reminders', verbose_name=_("Product"), help_text=_("Product for reminder"))  
    threshold = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Threshold"), help_text=_("Quantity threshold to trigger the reminder"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the reminder was set"))  

    objects = CustomFieldManager()  

    def __str__(self): return f"Reminder for {self.product} in {self.warehouse} at {self.threshold}"
    class Meta:
        verbose_name = _("Quantity Reminder") 
        verbose_name_plural = _("Quantity Reminders")  
        ordering = ['-created_at']  

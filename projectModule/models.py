from django.db import models
from django.utils.translation import gettext_lazy as _
from projectModule.models import Supplier 


class CustomFieldQuerySet(models.QuerySet):
    def custom_filter(self, **kwargs): return self.filter(**kwargs) 

class CustomFieldManager(models.Manager):
    def get_queryset(self): return CustomFieldQuerySet(self.model, using=self._db)
    def custom_filter(self, **kwargs): return self.get_queryset().custom_filter(**kwargs)


USAGE_CHOICES = [
    ('AG', _("Agricultural")),   
    ('AN', _("Animal")),         
    ('OT', _("Other")),        
]


class Asset(models.Model):
    asset_number = models.CharField(max_length=50, unique=True, verbose_name=_("Asset Number"), help_text=_("Unique identifier for the asset"))  
    name = models.CharField(max_length=255, verbose_name=_("Asset Name"), help_text=_("Name of the asset"))  
    purchase_date = models.DateField(verbose_name=_("Purchase/Creation Date"), help_text=_("Date of asset purchase or creation"))  
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"), help_text=_("Cost of the asset")) 
    usage = models.CharField(max_length=2, choices=USAGE_CHOICES, verbose_name=_("Usage"), help_text=_("Usage type (Agricultural, Animal, Other)"))  
    expected_lifetime = models.IntegerField(verbose_name=_("Expected Lifetime"), help_text=_("Expected lifetime of the asset in years"))  
    description = models.TextField(verbose_name=_("Description"), help_text=_("Additional details about the asset")) 
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Supplier/Person"), help_text=_("Responsible party for the asset")) 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the asset was added"))  

    objects = CustomFieldManager()  

    def __str__(self): return self.name
    class Meta:
        verbose_name = _("Asset")  
        verbose_name_plural = _("Assets")  
        ordering = ['asset_number']  


class Project(models.Model):
    project_number = models.CharField(max_length=50, unique=True, verbose_name=_("Project Number"), help_text=_("Unique identifier for the project"))  
    name = models.CharField(max_length=255, verbose_name=_("Project Name"), help_text=_("Name of the project"))  
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Asset"), help_text=_("Asset associated with the project (e.g., Agricultural land)"))  
    description = models.TextField(verbose_name=_("Description"), help_text=_("Additional details about the project"))  
    address = models.CharField(max_length=255, verbose_name=_("Address"), help_text=_("Location or address of the project"))  
    image = models.ImageField(upload_to='projects/', null=True, blank=True, verbose_name=_("Image"), help_text=_("Attach an illustrative image for the project"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the project was created")) 

    objects = CustomFieldManager()  

    def __str__(self): return self.name
    class Meta:
        verbose_name = _("Project")  
        verbose_name_plural = _("Projects") 
        ordering = ['project_number'] 


class ProjectCost(models.Model):
    cost_number = models.CharField(max_length=50, unique=True, verbose_name=_("Cost Number"), help_text=_("Unique identifier for the cost"))  
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='costs', verbose_name=_("Project"), help_text=_("Project to which the cost belongs")) 
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Asset"), help_text=_("Asset associated with the cost"))  
    name = models.CharField(max_length=255, verbose_name=_("Cost Name"), help_text=_("Name of the cost")) 
    description = models.TextField(verbose_name=_("Description"), help_text=_("Additional details about the cost")) 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the cost was added"))  

    objects = CustomFieldManager() 

    def __str__(self): return self.name
    class Meta:
        verbose_name = _("Project Cost") 
        verbose_name_plural = _("Project Costs")  
        ordering = ['cost_number']  

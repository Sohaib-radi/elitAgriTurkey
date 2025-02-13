from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomFieldQuerySet(models.QuerySet):
    def custom_filter(self, **kwargs):
        return self.filter(**kwargs)

class CustomFieldManager(models.Manager):
    def get_queryset(self):
        return CustomFieldQuerySet(self.model, using=self._db)
    def custom_filter(self, **kwargs):
        return self.get_queryset().custom_filter(**kwargs)


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Category Name"), help_text=_("Name of the category"))  
    description = models.TextField(verbose_name=_("Description"), help_text=_("Category description")) 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the category was created")) 

    objects = CustomFieldManager() 

    def __str__(self): return self.name
    class Meta:
        verbose_name = _("Product Category")  
        verbose_name_plural = _("Product Categories") 
        ordering = ['name'] 


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Product Name"), help_text=_("Name of the product")) 
    product_number = models.CharField(max_length=50, unique=True, verbose_name=_("Product Number"), help_text=_("Unique product number")) 
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products', verbose_name=_("Category"), help_text=_("Product category"))  
    description = models.TextField(verbose_name=_("Description"), help_text=_("Product description")) 
    benefit = models.TextField(verbose_name=_("Benefit"), help_text=_("Product benefit"))  
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Weight"), help_text=_("Product weight"))  
    usage_duration = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Usage Duration"), help_text=_("Usage duration or effectiveness"))  
    product_age = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Product Age"), help_text=_("Age of the product"))  
    storage_instructions = models.TextField(null=True, blank=True, verbose_name=_("Storage Instructions"), help_text=_("Instructions for storing the product"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the product was created"))  

    objects = CustomFieldManager() 

    def __str__(self): return f"{self.name} ({self.product_number})"
    class Meta:
        verbose_name = _("Product")  
        verbose_name_plural = _("Products") 
        ordering = ['-created_at']  
        indexes = [models.Index(fields=['product_number'], name='idx_product_number')]  


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name=_("Product"), help_text=_("Product this variant belongs to")) 
    name = models.CharField(max_length=255, verbose_name=_("Variant Name"), help_text=_("Name of the variant")) 
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Additional Price"), help_text=_("Additional price for the variant"))  
    sku = models.CharField(max_length=50, unique=True, verbose_name=_("SKU"), help_text=_("Stock Keeping Unit")) 

    objects = CustomFieldManager() 

    def __str__(self): return f"{self.product.name} - {self.name}"
    class Meta:
        verbose_name = _("Product Variant") 
        verbose_name_plural = _("Product Variants")  
        ordering = ['sku'] 


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_("Product"), help_text=_("Product for this image"))  
    image = models.ImageField(upload_to='product_images/', verbose_name=_("Image"), help_text=_("Product image file"))  
    alt_text = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Alt Text"), help_text=_("Alternative text for the image"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the image was added"))  

    objects = CustomFieldManager() 

    def __str__(self): return f"Image for {self.product.name}"
    class Meta:
        verbose_name = _("Product Image")  
        verbose_name_plural = _("Product Images")
        ordering = ['-created_at'] 


class SupplierList(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("List Name"), help_text=_("Name of the supplier list")) 
    description = models.TextField(verbose_name=_("Description"), help_text=_("Description of the supplier list")) 
    image = models.ImageField(upload_to='supplier_lists/', null=True, blank=True, verbose_name=_("List Image"), help_text=_("Image for the supplier list")) 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the list was created")) 

    objects = CustomFieldManager() 

    def __str__(self): return self.name
    class Meta:
        verbose_name = _("Supplier List")  
        verbose_name_plural = _("Supplier Lists")  
        ordering = ['name'] 


class Supplier(models.Model):
    supplier_number = models.CharField(max_length=50, unique=True, verbose_name=_("Supplier Number"), help_text=_("Unique supplier number"))  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='suppliers', verbose_name=_("Product"), help_text=_("Related product")) 
    supplier_name = models.CharField(max_length=255, verbose_name=_("Supplier Name"), help_text=_("Name of the supplier")) 
    company_name = models.CharField(max_length=255, verbose_name=_("Company Name"), help_text=_("Name of the company")) 
    supplier_list = models.ForeignKey(SupplierList, on_delete=models.SET_NULL, null=True, blank=True, related_name='suppliers', verbose_name=_("Supplier List"), help_text=_("Associated supplier list (e.g., Fuel)"))  
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"), help_text=_("Price of the product from this supplier")) 
    phone = models.CharField(max_length=20, verbose_name=_("Phone Number"), help_text=_("Supplier phone number"))  
    address = models.TextField(verbose_name=_("Address"), help_text=_("Supplier address"))  
    payment_method = models.CharField(max_length=100, verbose_name=_("Payment Method"), help_text=_("Method of payment"))  
    notes = models.TextField(null=True, blank=True, verbose_name=_("Notes"), help_text=_("Additional notes"))  
    product_image = models.ImageField(upload_to='supplier_products/', null=True, blank=True, verbose_name=_("Product Image"), help_text=_("Image of the product from the supplier"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the supplier record was created"))  

    objects = CustomFieldManager()  

    def __str__(self): return f"{self.supplier_name} - {self.company_name}"
    class Meta:
        verbose_name = _("Supplier")  
        verbose_name_plural = _("Suppliers")  
        ordering = ['-created_at'] 
        indexes = [models.Index(fields=['supplier_number'], name='idx_supplier_number')]  

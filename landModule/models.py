from django.db import models
#from django.contrib.gis.db.models import PointField  # For geolocation
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.contrib.auth import get_user_model
import uuid
User = get_user_model()


class LandType(models.TextChoices):
    AGRICULTURAL = "agricultural", _("Agricultural")
    RESIDENTIAL = "residential", _("Residential")
    COMMERCIAL = "commercial", _("Commercial")
    INDUSTRIAL = "industrial", _("Industrial")


class LandStatus(models.TextChoices):
    AVAILABLE = "available", _("Available")
    PLOWED = "plowed", _("Plowed")
    RENTED = "rented", _("Rented")
    CULTIVATED = "cultivated", _("Cultivated")



class Wilaya(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Wilaya Name"))

    class Meta:
        verbose_name = _("Wilaya")
        verbose_name_plural = _("Wilayas")
        ordering = ["name"]

    def __str__(self):
        return self.name



class Land(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique ID
    international_number = models.CharField(max_length=100, unique=True, verbose_name=_("International Land Number"))
    land_number = models.CharField(max_length=100, default="ddd",  verbose_name=_("Land Number"))
    #aria_number = models.CharField(max_length=100, unique=True, verbose_name=_("Aria Number"))
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, related_name="lands", verbose_name=_("Wilaya"))
    address = models.TextField(verbose_name=_("Address"))
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Price (USD)"))
    purchase_date = models.DateTimeField(default=now, verbose_name=_("Purchase Date"))
    land_type = models.CharField(max_length=20, choices=LandType.choices, verbose_name=_("Land Type"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Area (sqm)"))
    #location = PointField(geography=True, blank=True, null=True, verbose_name=_("Geolocation"))
    status = models.CharField(max_length=20, choices=LandStatus.choices, default=LandStatus.AVAILABLE, verbose_name=_("Land Status"))
    #TODO: Add MOUHIT FOR LAND ( FOR EXAMPLE: THE LAND)
    #TODO: Add DATE OF PURCHASE
    #TODO: MANAGE PURCHASE OF LAND 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))
    current_owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="owned_lands",
        verbose_name="Current Owner"
    )
    previous_owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="previously_owned_lands",
        verbose_name="Previous Owner"
    )
    purchase_date = models.DateTimeField(default=now, verbose_name="Purchase Date")
    def mark_as_sold(self, buyer):
        """ Marks the land as sold and updates ownership """
        self.previous_owner = self.current_owner   
        self.current_owner = buyer   
        self.status = "Sold"
        self.save()
    class Meta:
        verbose_name = _("Land")
        verbose_name_plural = _("Lands")
        indexes = [
            models.Index(fields=["international_number"]),
            models.Index(fields=["land_number"]),
            models.Index(fields=["wilaya"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.land_number} - {self.wilaya.name}"


    def get_absolute_url(self):
        return f"/lands/{self.id}/"

    def get_status_display(self):
        return dict(LandStatus.choices).get(self.status, "Unknown")



class LandDocument(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name="documents", verbose_name=_("Land"))
    title = models.CharField(max_length=255, verbose_name=_("Document Title"))
    file = models.FileField(upload_to="land_documents/", verbose_name=_("Document File"))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))

    class Meta:
        verbose_name = _("Land Document")
        verbose_name_plural = _("Land Documents")
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title


class LandImage(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name="images", verbose_name=_("Land"), null=True, blank=True)
    image = models.ImageField(upload_to="land_images/", verbose_name=_("Land Image"), null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"), null=True, blank=True)

    class Meta:
        verbose_name = _("Land Image")
        verbose_name_plural = _("Land Images")
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Image for {self.land.land_number}"

class LandTransaction(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name='transactions', verbose_name=_("Land"))
    transaction_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Transaction Date"))
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name=_("Price (USD)"))
    buyer_name = models.CharField(max_length=255, verbose_name=_("Buyer Name"), blank=True, null=True)
    buyer_phone = models.CharField(max_length=255, verbose_name=_("Buyer Phone") , blank=True, null=True)
    buyer_email = models.EmailField(max_length=255, verbose_name=_("Buyer Email") , blank=True, null=True)
    buyer_address = models.TextField(verbose_name=_("Buyer Address") , blank=True, null=True)
    purchase_date = models.DateTimeField(default=now , verbose_name=_("Purchase Date") , blank=True, null=True) 
    payment_status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Completed", "Completed")],
        default="Pending"
    )  
    def complete_purchase(self):
        """ Mark purchase as completed and update land status """
        self.payment_status = "Completed"
        self.land.mark_as_sold(self.buyer)
        self.save() 
    class Meta:
        verbose_name = _('Land Transaction')
        verbose_name_plural = _('Land Transactions')

    def __str__(self):
        return f"Transaction for {self.land} by {self.buyer_name}"

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', _('Create')),
        ('UPDATE', _('Update')),
        ('DELETE', _('Delete')),
        ('STATUS_CHANGE', _('Status Change')),
    ]
    
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    action_timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=255, null=True, blank=True)
    details = models.TextField()

    class Meta:
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')

    def __str__(self):
        return f"Audit Log for {self.land}"

class LandQuerySet(models.QuerySet):
    def by_wilaya(self, wilaya_id):
        return self.filter(wilaya_id=wilaya_id)

    def by_status(self, status):
        return self.filter(status=status)

    def search(self, query):
        return self.filter(models.Q(international_number__icontains=query) | models.Q(land_number__icontains=query))



class LandManager(models.Manager):
    def get_queryset(self):
        return LandQuerySet(self.model, using=self._db)

    def available_lands(self):
        return self.get_queryset().by_status(LandStatus.AVAILABLE)

    def plowed_lands(self):
        return self.get_queryset().by_status(LandStatus.PLOWED)

    def rented_lands(self):
        return self.get_queryset().by_status(LandStatus.RENTED)
    def filter_by_state(self, state_name):
        return self.filter(state__name=state_name)

    def filter_by_land_type(self, land_type):
        return self.filter(land_type=land_type)

    def filter_by_area(self, min_area=None, max_area=None):
        query = self.all()
        if min_area:
            query = query.filter(area__gte=min_area)
        if max_area:
            query = query.filter(area__lte=max_area)
        return query

    def filter_by_transaction_date(self, start_date, end_date):
        return self.filter(transactions__transaction_date__range=[start_date, end_date])

Land.objects = LandManager()

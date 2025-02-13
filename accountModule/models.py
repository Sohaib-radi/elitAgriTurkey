# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin Profile'),
        ('farm', 'Farm Profile'),
        ('farmmanager', 'Farm Manager'),
        ('user', 'User Profile'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name=_("User Profile"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    residence_location = models.CharField(max_length=255, verbose_name=_("Residence Location"))
    
    profile_picture = models.ImageField( upload_to="users/profile_pictures/", blank=True, null=True, verbose_name=_("Profile Picture"))
    def __str__(self):
        return self.username


# Payment Installment model
class PaymentInstallment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='installments'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    initial_payment = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PaymentInstallment for {self.user.username} - Total: {self.total_amount}"


# Optional: A schedule model to track individual installment payments
class PaymentInstallmentSchedule(models.Model):
    installment = models.ForeignKey(
        PaymentInstallment,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Installment due {self.due_date} - Amount: {self.amount_due}"


# Review/Rating model to allow users to review one another
class Review(models.Model):
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )
    reviewee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews'
    )
    rating = models.PositiveIntegerField()  # e.g., rating on a scale of 1-5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Optionally restrict so a user can only review another user once per transaction/relationship.
        unique_together = ('reviewer', 'reviewee')

    def __str__(self):
        return f"Review from {self.reviewer.username} to {self.reviewee.username}"
    
    
    

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True, verbose_name=_("Bio"))
    bank_account_number = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Bank Account Number"))
    credit_card_token = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Credit Card Token"))
    # Add any additional fields here

    def __str__(self):
        return f"{self.user.username}'s Profile"
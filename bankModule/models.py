from django.db import models
from django.utils.translation import gettext_lazy as _

class BankManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('name')

class Bank(models.Model):
    bank_number = models.CharField(_("Bank Number"), max_length=50, unique=True)
    name = models.CharField(_("Bank Name"), max_length=100)
    account_number = models.CharField(_("Account Number"), max_length=50)
    branch_name = models.CharField(_("Branch Name"), max_length=100)
    address = models.TextField(_("Address"))
    phone = models.CharField(_("Phone Number"), max_length=20)
    email = models.EmailField(_("Email"))
    currency = models.CharField(_("Main Currency"), max_length=10)
    description = models.TextField(_("Description"), blank=True)

    objects = BankManager()

    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")
        ordering = ['name']

    def __str__(self):
        return self.name

class LoanManager(models.Manager):
    def paid_loans(self):
        return self.filter(status=Loan.Status.PAID)
    
    def unpaid_loans(self):
        return self.filter(status=Loan.Status.UNPAID)
    
    def overdue_loans(self):
        return self.filter(status=Loan.Status.OVERDUE)

class Loan(models.Model):
    class PaymentMethod(models.TextChoices):
        BANK_TRANSFER = 'transfer', _('Bank Transfer')
        CASH = 'cash', _('Cash')
        CHEQUE = 'cheque', _('Cheque')

    class Status(models.TextChoices):
        PAID = 'paid', _('Paid')
        UNPAID = 'unpaid', _('Unpaid')
        OVERDUE = 'overdue', _('Overdue')

    loan_number = models.CharField(_("Loan Number"), max_length=50, unique=True)
    name = models.CharField(_("Loan Name"), max_length=100)
    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        verbose_name=_("Related Bank"),
        related_name='loans'
    )
    amount = models.DecimalField(
        _("Loan Amount"),
        max_digits=15,
        decimal_places=2
    )
    receipt_date = models.DateField(_("Receipt Date"))
    duration = models.PositiveIntegerField(_("Loan Duration (months)"))
    interest_rate = models.DecimalField(
        _("Interest Rate"),
        max_digits=5,
        decimal_places=2
    )
    payment_method = models.CharField(
        _("Payment Method"),
        max_length=20,
        choices=PaymentMethod.choices
    )
    installments_count = models.PositiveIntegerField(_("Number of Installments"))
    installment_amount = models.DecimalField(
        _("Installment Amount"),
        max_digits=15,
        decimal_places=2
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=Status.choices,
        default=Status.UNPAID
    )

    objects = LoanManager()

    class Meta:
        verbose_name = _("Loan")
        verbose_name_plural = _("Loans")
        ordering = ['-receipt_date']

    def __str__(self):
        return f"{self.name} - {self.loan_number}"

class Installment(models.Model):
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        verbose_name=_("Loan"),
        related_name='installments'
    )
    due_date = models.DateField(_("Due Date"))
    amount = models.DecimalField(
        _("Amount"),
        max_digits=15,
        decimal_places=2
    )
    paid_date = models.DateField(_("Paid Date"), null=True, blank=True)
    is_paid = models.BooleanField(_("Is Paid"), default=False)

    class Meta:
        verbose_name = _("Installment")
        verbose_name_plural = _("Installments")
        ordering = ['due_date']

    def __str__(self):
        return f"Installment #{self.id} for {self.loan}"

class LoanReport(models.Model):
    report_date = models.DateField(_("Report Date"), auto_now_add=True)
    total_loans = models.DecimalField(
        _("Total Loans"),
        max_digits=15,
        decimal_places=2
    )
    paid_installments = models.PositiveIntegerField(_("Paid Installments"))
    unpaid_installments = models.PositiveIntegerField(_("Unpaid Installments"))
    overdue_loans = models.PositiveIntegerField(_("Overdue Loans"))
    total_interest = models.DecimalField(
        _("Total Interest"),
        max_digits=15,
        decimal_places=2
    )

    class Meta:
        verbose_name = _("Loan Report")
        verbose_name_plural = _("Loan Reports")
        ordering = ['-report_date']

    def __str__(self):
        return f"Loan Report - {self.report_date}"
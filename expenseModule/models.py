from django.db import models
from django.utils.translation import gettext_lazy as _
from productModule.models import Supplier  
from productModule.models import Product  

 
class CustomFieldQuerySet(models.QuerySet):
    def custom_filter(self, **kwargs): return self.filter(**kwargs)   

class CustomFieldManager(models.Manager):
    def get_queryset(self): return CustomFieldQuerySet(self.model, using=self._db)
    def custom_filter(self, **kwargs): return self.get_queryset().custom_filter(**kwargs)
 
class ExpenseList(models.Model):
    list_name = models.CharField(max_length=255, verbose_name=_("List Name"), help_text=_("Name of the expense list"))  
    list_number = models.CharField(max_length=50, unique=True, verbose_name=_("List Number"), help_text=_("Unique identifier for the expense list"))   
    expense_type = models.CharField(max_length=100, verbose_name=_("Expense Type"), help_text=_("Type of expense"))   
    monthly_expense = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Monthly Expense"), help_text=_("Monthly expense budget"))  
    image = models.ImageField(upload_to='expense_lists/', null=True, blank=True, verbose_name=_("Image"), help_text=_("Attach an image"))   
    description = models.TextField(verbose_name=_("Description"), help_text=_("Description of the expense list")) 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the expense list was created"))   

    objects = CustomFieldManager()  

    def __str__(self): return self.list_name
    class Meta:
        verbose_name = _("Expense List")   
        verbose_name_plural = _("Expense Lists")  
        ordering = ['list_number']   

 
class ExpenseItem(models.Model):
    expense_number = models.CharField(max_length=50, unique=True, verbose_name=_("Expense Number"), help_text=_("Unique identifier for the expense item"))  
    name = models.CharField(max_length=255, verbose_name=_("Expense Name"), help_text=_("Name of the expense or its reference number"))  
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"), help_text=_("Amount of the expense"))  
    description = models.TextField(verbose_name=_("Description"), help_text=_("Additional details about the expense")) 
    date = models.DateField(verbose_name=_("Date"), help_text=_("Date of the expense"))  
    status = models.CharField(max_length=50, verbose_name=_("Status"), help_text=_("Status of the expense (e.g. pending, approved)"))  
    expense_list = models.ForeignKey(ExpenseList, on_delete=models.CASCADE, related_name='expenses', verbose_name=_("Expense List"), help_text=_("Associated expense list"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the expense was added"))   

    objects = CustomFieldManager()  

    def __str__(self): return self.name
    class Meta:
        verbose_name = _("Expense Item")  
        verbose_name_plural = _("Expense Items")   
        ordering = ['date']  

 
class ReceiptVoucher(models.Model):
 
    buyer = models.ForeignKey('Buyer', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Buyer"), help_text=_("Buyer (FK)"))   
    voucher_number = models.CharField(max_length=50, unique=True, verbose_name=_("Voucher Number"), help_text=_("Unique receipt voucher number"))   
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"), help_text=_("Amount received"))   
    date = models.DateField(verbose_name=_("Date"), help_text=_("Date of the receipt voucher"))  
    description = models.TextField(verbose_name=_("Description"), help_text=_("Details about the voucher"))  
    receiver_signature = models.CharField(max_length=255, verbose_name=_("Receiver Signature"), help_text=_("Signature of the receiver"))  
    accountant_signature = models.CharField(max_length=255, verbose_name=_("Accountant Signature"), help_text=_("Signature of the accountant"))   
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the voucher was created"))   

    objects = CustomFieldManager()   

    def __str__(self): return self.voucher_number
    class Meta:
        verbose_name = _("Receipt Voucher")   
        verbose_name_plural = _("Receipt Vouchers")   
        ordering = ['voucher_number']   

 
class PaymentVoucher(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Supplier"), help_text=_("Supplier (FK)"))  
    voucher_number = models.CharField(max_length=50, unique=True, verbose_name=_("Voucher Number"), help_text=_("Unique payment voucher number"))   
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"), help_text=_("Amount paid"))   
    description = models.TextField(verbose_name=_("Description"), help_text=_("Details about the voucher"))  
    date = models.DateField(verbose_name=_("Date"), help_text=_("Date of the payment voucher"))  
    accountant_signature = models.CharField(max_length=255, verbose_name=_("Accountant Signature"), help_text=_("Signature of the accountant"))   
    receiver_signature = models.CharField(max_length=255, verbose_name=_("Receiver Signature"), help_text=_("Signature of the receiver"))   
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the voucher was created"))  

    objects = CustomFieldManager()   

    def __str__(self): return self.voucher_number
    class Meta:
        verbose_name = _("Payment Voucher")  
        verbose_name_plural = _("Payment Vouchers")   
        ordering = ['voucher_number']  

 
class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True, verbose_name=_("Order Number"), help_text=_("Unique order number"))   
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Supplier"), help_text=_("Supplier associated with the order (FK)"))  
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Product"), help_text=_("Product associated with the order (FK)"))  
    date = models.DateField(verbose_name=_("Date"), help_text=_("Date of the order"))  
    accountant_signature = models.CharField(max_length=255, verbose_name=_("Accountant Signature"), help_text=_("Signature of the accountant"))   
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the order was created"))  

    objects = CustomFieldManager()   

    def __str__(self): return self.order_number
    class Meta:
        verbose_name = _("Order")   
        verbose_name_plural = _("Orders")   
        ordering = ['order_number']   

 
class RevenueList(models.Model):
    list_name = models.CharField(max_length=255, verbose_name=_("Revenue List Name"), help_text=_("Name of the revenue list"))  # اسم القائمة
    list_number = models.CharField(max_length=50, unique=True, verbose_name=_("List Number"), help_text=_("Unique number for the revenue list"))  # رقم القائمة
    associated_number = models.CharField(max_length=50, verbose_name=_("Associated Number"), help_text=_("Associated number (e.g., project, product)"))  # رقم مرتبط
    description = models.TextField(verbose_name=_("Description"), help_text=_("Description of the revenue list"))  # الوصف
    image = models.ImageField(upload_to='revenue_lists/', null=True, blank=True, verbose_name=_("Image"), help_text=_("Attach an image"))  # إرفاق صورة
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the revenue list was created"))  # تاريخ الإنشاء

    objects = CustomFieldManager()  

    def __str__(self): return self.list_name
    class Meta:
        verbose_name = _("Revenue List")  
        verbose_name_plural = _("Revenue Lists")  
        ordering = ['list_number']  

 
class RevenueItem(models.Model):
    revenue_list = models.ForeignKey(RevenueList, on_delete=models.CASCADE, related_name='revenues', verbose_name=_("Revenue List"), help_text=_("Associated revenue list (FK)"))   
    item_number = models.CharField(max_length=50, unique=True, verbose_name=_("Item Number"), help_text=_("Unique identifier for the revenue item"))  
    description = models.TextField(verbose_name=_("Description"), help_text=_("Description of the revenue item"))  
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"), help_text=_("Amount of revenue"))  
    date = models.DateField(verbose_name=_("Date"), help_text=_("Date of the revenue item"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the revenue item was added"))  

    objects = CustomFieldManager()  

    def __str__(self): return self.item_number
    class Meta:
        verbose_name = _("Revenue Item") 
        verbose_name_plural = _("Revenue Items")   
        ordering = ['date']   

 
SERVICE_CHOICES = [
    ('WTR', _("Water")),    
    ('ELE', _("Electricity")),   
    ('GAS', _("Gas")),      
    ('OT', _("Other")),     
]

class Company(models.Model):
    company_number = models.CharField(max_length=50, unique=True, verbose_name=_("Company Number"), help_text=_("Unique identifier for the company"))   
    company_name = models.CharField(max_length=255, verbose_name=_("Company Name"), help_text=_("Name of the company"))  
    branch_name = models.CharField(max_length=255, verbose_name=_("Branch Name"), help_text=_("Name of the branch"))  
    branch_address = models.CharField(max_length=255, verbose_name=_("Branch Address"), help_text=_("Address of the branch"))  
    phone = models.CharField(max_length=20, verbose_name=_("Phone"), help_text=_("Phone number"))  
    description = models.TextField(verbose_name=_("Description"), help_text=_("Additional details")) 
    service = models.CharField(max_length=3, choices=SERVICE_CHOICES, verbose_name=_("Service"), help_text=_("Service type (Water, Electricity, Gas, Other)"))   
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the company was registered"))   

    objects = CustomFieldManager()  

    def __str__(self): return self.company_name
    class Meta:
        verbose_name = _("Company")  
        verbose_name_plural = _("Companies")   
        ordering = ['company_number']   

 
class Subscription(models.Model):
    subscription_name = models.CharField(max_length=255, verbose_name=_("Subscription Name"), help_text=_("Name of the subscription"))   
    subscription_number = models.CharField(max_length=50, unique=True, verbose_name=_("Subscription Number"), help_text=_("Unique identifier for the subscription"))   
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Company"), help_text=_("Associated company (FK)"))   
    subscription_account_number = models.CharField(max_length=50, verbose_name=_("Account Number"), help_text=_("Subscription account number"))  
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Monthly Amount"), help_text=_("Monthly subscription amount"))   
    payment_method = models.CharField(max_length=100, verbose_name=_("Payment Method"), help_text=_("Method of payment"))  
    start_date = models.DateField(verbose_name=_("Start Date"), help_text=_("Subscription start date"))   
    end_date = models.DateField(verbose_name=_("End Date"), help_text=_("Subscription end date"))   
    description = models.TextField(verbose_name=_("Description"), help_text=_("Additional details"))  
    address = models.CharField(max_length=255, verbose_name=_("Address"), help_text=_("Address associated with the subscription"))   
    image = models.ImageField(upload_to='subscriptions/', null=True, blank=True, verbose_name=_("Image"), help_text=_("Attach an image (optional)"))   
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the subscription was created"))  

    objects = CustomFieldManager()   

    def __str__(self): return self.subscription_name
    class Meta:
        verbose_name = _("Subscription")  
        verbose_name_plural = _("Subscriptions")  
        ordering = ['subscription_number']  

#  Subscription Report views
 
 
DEBT_STATUS_CHOICES = [
    ('DUE', _("Due")),           
    ('PART', _("Partially Paid")),  
    ('FULL', _("Fully Paid")),   
]

class Debt(models.Model):
    debtor_number = models.CharField(max_length=50, verbose_name=_("Debtor Number"), help_text=_("Number of buyer, supplier, person, or employee associated with the debt"))   
    name = models.CharField(max_length=255, verbose_name=_("Name"), help_text=_("Name of the debtor"))   
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"), help_text=_("Value of the debt"))   
    debt_reason = models.TextField(verbose_name=_("Debt Reason"), help_text=_("Purpose of the debt"))   
    due_date = models.DateField(verbose_name=_("Due Date"), help_text=_("Due date for debt repayment"))   
    debt_status = models.CharField(max_length=4, choices=DEBT_STATUS_CHOICES, verbose_name=_("Debt Status"), help_text=_("Status of the debt"))   
    description = models.TextField(verbose_name=_("Description"), help_text=_("Additional details about the debt"))  
    image = models.ImageField(upload_to='debts/', null=True, blank=True, verbose_name=_("Image"), help_text=_("Attach an image of related documents"))   
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the debt was recorded"))   

    objects = CustomFieldManager()  

    def __str__(self): return self.debtor_number
    class Meta:
        verbose_name = _("Debt") 
        verbose_name_plural = _("Debts")  
        ordering = ['due_date'] 

 
class Buyer(models.Model):
    buyer_name = models.CharField(max_length=255, verbose_name=_("Buyer Name"), help_text=_("Name of the buyer"))  
    buyer_number = models.CharField(max_length=50, unique=True, verbose_name=_("Buyer Number"), help_text=_("Unique buyer number"))   
    phone = models.CharField(max_length=20, verbose_name=_("Phone"), help_text=_("Phone number of the buyer"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the buyer was registered"))   

    objects = CustomFieldManager()  

    def __str__(self): return self.buyer_name
    class Meta:
        verbose_name = _("Buyer")   
        verbose_name_plural = _("Buyers")  
        ordering = ['buyer_number']   

 
class SaleTransaction(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Buyer"), help_text=_("Buyer (FK)"))   
    sale_number = models.CharField(max_length=50, unique=True, verbose_name=_("Sale Number"), help_text=_("Unique identifier for the sale"))  
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Product"), help_text=_("Product sold (FK)"))  
    sale_place = models.CharField(max_length=255, verbose_name=_("Sale Place"), help_text=_("Place where the sale occurred"))   
    address = models.CharField(max_length=255, verbose_name=_("Address"), help_text=_("Address of the sale"))   
    phone = models.CharField(max_length=20, verbose_name=_("Phone"), help_text=_("Phone number for contact"))   
    date = models.DateField(verbose_name=_("Date"), help_text=_("Date of the sale")) 
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"), help_text=_("Quantity sold"))  
    total_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Value"), help_text=_("Total sales value"))   
    price_per_product = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price Per Product"), help_text=_("Price for each product"))   
    payment_method = models.CharField(max_length=100, verbose_name=_("Payment Method"), help_text=_("Payment method used"))  
    delivery_date = models.DateField(verbose_name=_("Delivery Date"), help_text=_("Date of delivery"))   
    vat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("VAT"), help_text=_("Calculated VAT based on sale value"))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the sale was recorded"))   

    objects = CustomFieldManager()  

    def __str__(self): return self.sale_number
    class Meta:
        verbose_name = _("Sale Transaction")   
        verbose_name_plural = _("Sale Transactions")  
        ordering = ['sale_number']  

 
class PurchaseTransaction(models.Model):
    purchase_number = models.CharField(max_length=50, unique=True, verbose_name=_("Purchase Number"), help_text=_("Unique identifier for the purchase transaction"))   
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Supplier"), help_text=_("Supplier (FK)"))  
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Product"), help_text=_("Product purchased (FK)")) 
    address = models.CharField(max_length=255, verbose_name=_("Address"), help_text=_("Address related to the purchase"))   
    date = models.DateField(verbose_name=_("Date"), help_text=_("Date of the purchase"))  
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"), help_text=_("Quantity purchased"))  
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount"), help_text=_("Amount of the purchase"))   
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the purchase transaction was recorded"))  

    objects = CustomFieldManager()   

    def __str__(self): return self.purchase_number
    class Meta:
        verbose_name = _("Purchase Transaction") 
        verbose_name_plural = _("Purchase Transactions")   
        ordering = ['purchase_number']  

 
class PurchaseTransactionDetail(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Supplier"), help_text=_("Supplier associated with the transaction detail"))   
    payment_method = models.CharField(max_length=100, verbose_name=_("Payment Method"), help_text=_("Method of payment used"))   
    payment_terms = models.CharField(max_length=255, verbose_name=_("Payment Terms"), help_text=_("Payment terms (e.g., cash, installment)"))   
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Total Amount"), help_text=_("Total amount due to the supplier"))   
    total_transactions = models.PositiveIntegerField(verbose_name=_("Total Transactions"), help_text=_("Total number of transactions with the supplier"))  
    amount_per_transaction = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount Per Transaction"), help_text=_("Amount for each individual transaction"))   
    transaction_date = models.DateField(verbose_name=_("Transaction Date"), help_text=_("Date of the transaction"))   
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"), help_text=_("Date when the transaction detail was added"))   

    objects = CustomFieldManager()   

    def __str__(self): return f"Detail for {self.supplier}"
    class Meta:
        verbose_name = _("Purchase Transaction Detail")  
        verbose_name_plural = _("Purchase Transaction Details")   
        ordering = ['transaction_date']   

 
 
 
 
# 1. Budget Report 
# 2. Profitability Report  
# 3. Financial Reports  
# 4. Tax Report  


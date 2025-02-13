from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _



class DepartmentChoices(models.TextChoices):
    ANIMAL = "Animal", _("Animal")
    AGRICULTURAL = "Agricultural", _("Agricultural")
    OTHER = "Other", _("Other")
#TODO: Add Department MODEL  -- > DONE
class Department(models.Model):
    name = models.CharField(
        max_length=50,
        choices=DepartmentChoices.choices,
        unique=True,
        verbose_name=_("Department Name")
    )
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        ordering = ["name"]

    def __str__(self):
        return self.get_name_display()


class MaritalStatus(models.TextChoices):
    SINGLE = "Single", _("Single")
    MARRIED = "Married", _("Married")

class EmployeeStatus(models.TextChoices):
    ACTIVE = "Active", _("Active")
    INACTIVE = "Inactive", _("Inactive")
    ON_LEAVE = "On Leave", _("On Leave")
    RESIGNED = "Resigned", _("Resigned")

#TODO : Add Employee MANAGEMENT SYSTEM
class Employee(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    employee_id = models.CharField(max_length=50, unique=True, verbose_name=_("Employee ID"))
    department = models.ForeignKey(
            Department,
            on_delete=models.SET_NULL,  
            null=True,
            blank=True,
            related_name="employees",
            verbose_name=_("Department")
        )
    job_title = models.CharField(max_length=255, verbose_name=_("Job Title"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Phone Number"))
    residence_location = models.CharField(max_length=255, verbose_name=_("Residence Location"))
    monthly_salary = models.DecimalField( max_digits=10, decimal_places=2, verbose_name=_("Monthly Salary"))
    additional_notes = models.TextField(blank=True, null=True, verbose_name=_("Additional Notes"))
    profile_picture = models.ImageField( upload_to="employees/profile_pictures/", blank=True, null=True, verbose_name=_("Profile Picture"))
    age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)], verbose_name=_("Age"))
    work_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=_("Work Latitude"))
    work_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=_("Work Longitude") )
    marital_status = models.CharField( max_length=10, choices=MaritalStatus.choices, verbose_name=_("Marital Status"))
    annual_leave_allowance = models.PositiveIntegerField( default=30, verbose_name=_("Annual Leave Allowance"))
    status = models.CharField(max_length=20, choices=EmployeeStatus.choices, default=EmployeeStatus.ACTIVE, verbose_name=_("Status"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.employee_id})"

    def get_location(self):
        """Returns the employee's work location as a dictionary."""
        return {"latitude": self.work_latitude, "longitude": self.work_longitude}

    def update_status(self, new_status):
        """Updates the employee's status."""
        if new_status in EmployeeStatus.values:
            self.status = new_status
            self.save()
            return True
        return False

    def calculate_remaining_leaves(self, used_leaves):
        """Calculates the remaining leave days for the employee."""
        return max(self.annual_leave_allowance - used_leaves, 0)

#TODO: Add Employee Document TYPE AND CATEGORYSED -- > DONE

class DocumentType(models.TextChoices):
    CONTRACT = "Contract", _("Contract")
    CERTIFICATE = "Certificate", _("Certificate")
    IDENTITY = "Identity", _("Identity")
    OTHER = "Other", _("Other")
    
class DocumentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Category Name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Document Category")
        verbose_name_plural = _("Document Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name
class EmployeeDocument(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="documents", verbose_name=_("Employee")
    )
    document_name = models.CharField(max_length=255, verbose_name=_("Document Name"))
    document_type = models.CharField(
        max_length=50,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
        verbose_name=_("Document Type")
    )
    category = models.ForeignKey(
        DocumentCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Category")
    )
    file = models.FileField(upload_to="employees/documents/", verbose_name=_("File"))
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Uploaded At"))

    class Meta:
        verbose_name = _("Employee Document")
        verbose_name_plural = _("Employee Documents")

    def __str__(self):
        return f"{self.document_name} ({self.get_document_type_display()}) - {self.employee.first_name} {self.employee.last_name}"
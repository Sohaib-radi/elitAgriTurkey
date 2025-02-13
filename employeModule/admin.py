from django.contrib import admin
from .models import Employee, EmployeeDocument,Department, DocumentCategory

admin.site.register(Employee)
admin.site.register(EmployeeDocument)
admin.site.register(Department)
admin.site.register(DocumentCategory)

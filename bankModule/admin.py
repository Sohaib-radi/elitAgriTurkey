from django.contrib import admin
from .models import Bank, Loan,Installment, LoanReport

admin.site.register(Bank)
admin.site.register(Loan)
admin.site.register(Installment)
admin.site.register(LoanReport)

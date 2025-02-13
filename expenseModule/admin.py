from django.contrib import admin
from .models import ExpenseList, ExpenseItem,ReceiptVoucher, PaymentVoucher,Order,RevenueList,RevenueItem,Company,Subscription,Debt,Buyer,SaleTransaction,PurchaseTransaction,PurchaseTransactionDetail

admin.site.register(ExpenseList)
admin.site.register(ExpenseItem)
admin.site.register(ReceiptVoucher)
admin.site.register(PaymentVoucher)
admin.site.register(Order)
admin.site.register(RevenueList)
admin.site.register(RevenueItem)
admin.site.register(Company)
admin.site.register(Subscription)
admin.site.register(Debt)
admin.site.register(Buyer)
admin.site.register(SaleTransaction)
admin.site.register(PurchaseTransaction)
admin.site.register(PurchaseTransactionDetail)





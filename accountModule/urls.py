from django.urls import path, include
from rest_framework import routers
from .views import CustomTokenObtainPairView, PaymentInstallmentViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register(r'payment-installments', PaymentInstallmentViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]

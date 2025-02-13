from rest_framework import generics, viewsets, permissions
from .models import CustomUser, PaymentInstallment, Review
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .serializers import (
    CustomUserSerializer,
    PaymentInstallmentSerializer,
    ReviewSerializer,
    CustomTokenObtainPairSerializer
)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated successfully!"})
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Registration endpoint for new users
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]


# ViewSet for managing payment installments
class PaymentInstallmentViewSet(viewsets.ModelViewSet):
    queryset = PaymentInstallment.objects.all()
    serializer_class = PaymentInstallmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the owner of the installment.
        serializer.save(user=self.request.user)


# ViewSet for managing reviews
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the current user as the reviewer.
        serializer.save(reviewer=self.request.user)
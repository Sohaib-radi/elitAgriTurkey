from rest_framework import serializers
from .models import CustomUser, PaymentInstallment, PaymentInstallmentSchedule, Review
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# User serializer with write-only password field
class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role', 'phone_number']

    def create(self, validated_data):
        # Use Django’s create_user to handle password hashing and other logic.
        user = CustomUser.objects.create_user(**validated_data)
        return user


# Serializer for individual installment schedules
class PaymentInstallmentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInstallmentSchedule
        fields = ['id', 'due_date', 'amount_due', 'is_paid', 'paid_at']


# Serializer for payment installments
class PaymentInstallmentSerializer(serializers.ModelSerializer):
    # Nested representation for the schedule
    schedules = PaymentInstallmentScheduleSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PaymentInstallment
        fields = [
            'id', 'user', 'total_amount', 'initial_payment',
            'remaining_amount', 'created_at', 'schedules'
        ]


# Serializer for reviews; note that the reviewee ID is expected in the input.
class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    reviewee = serializers.StringRelatedField(read_only=True)
    reviewee_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'reviewee', 'reviewee_id', 'rating', 'comment', 'created_at']

    def create(self, validated_data):
        reviewee_id = validated_data.pop('reviewee_id')
        # Validate that the reviewee exists
        reviewee = CustomUser.objects.get(id=reviewee_id)
        review = Review.objects.create(reviewee=reviewee, **validated_data)
        return review

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        
        return token

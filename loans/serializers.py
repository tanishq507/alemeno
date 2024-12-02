from rest_framework import serializers
from .models import Customer, Loan

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'age', 'monthly_income', 
                 'phone_number', 'approved_limit']

class LoanEligibilitySerializer(serializers.Serializer):
    customer = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()

class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['customer', 'loan_amount', 'interest_rate', 'tenure']

class LoanDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Loan
        fields = ['id', 'customer', 'loan_amount', 'interest_rate', 
                 'tenure', 'emi', 'status']
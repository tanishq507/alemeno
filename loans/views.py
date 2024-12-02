from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Loan
from .serializers import (
    CustomerSerializer, LoanEligibilitySerializer,
    LoanCreateSerializer, LoanDetailSerializer
)
from decimal import Decimal

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            customer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check_eligibility(request):
    # Deserialize the request data
    serializer = LoanEligibilitySerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Extract validated data
    loan_data = serializer.validated_data
    
    # Call the second function to calculate eligibility and return response
    result = calculate_loan_eligibility(loan_data)
    return Response(result, status=status.HTTP_200_OK)

def calculate_loan_eligibility(loan_data):
    try:
        customer = Customer.objects.get(id=loan_data['customer'])
    except Customer.DoesNotExist:
        return {'status': 'REJECTED', 'message': 'Customer not found'}

    # Get loan details from the loan_data dictionary
    loan_amount = Decimal(loan_data['loan_amount'])
    interest_rate = Decimal(loan_data['interest_rate'])
    tenure = loan_data['tenure']  # tenure in months

    # Calculate EMI using the formula
    P = loan_amount
    R = interest_rate / (12 * Decimal('100'))  # Monthly interest rate
    N = tenure  # Loan tenure in months
    emi = P * R * (pow(1 + R, N)) / (pow(1 + R, N) - 1)

    # Check if EMI exceeds 50% of monthly salary
    if emi > (customer.monthly_income * Decimal('0.5')):
        return {
            'status': 'REJECTED',
            'message': 'EMI exceeds 50% of monthly salary'
        }

    # Credit score based approval logic
    if customer.credit_score > 50:
        approval_status = 'APPROVED'
    elif 30 < customer.credit_score <= 50:
        approval_status = 'APPROVED'
        interest_rate = max(interest_rate, Decimal('12.0'))  # Ensure interest rate is at least 12%
    elif 10 < customer.credit_score <= 30:
        approval_status = 'APPROVED'
        interest_rate = max(interest_rate, Decimal('16.0'))  # Ensure interest rate is at least 16%
    else:
        approval_status = 'REJECTED'

    # Return the result as a dictionary
    return {
        'status': approval_status,
        'interest_rate': round(interest_rate, 2),  # Round interest rate to 2 decimal places
        'tenure': tenure,
        'monthly_installment': round(emi, 2)  # Round EMI to 2 decimal places
    }

@api_view(['POST'])
def create_loan(request):
    serializer = LoanCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Check eligibility first
    eligibility_check = calculate_loan_eligibility(request.data)
    if eligibility_check['status'] == 'REJECTED':
        return Response(eligibility_check, status=status.HTTP_400_BAD_REQUEST)

    loan = serializer.save()
    loan.emi = loan.calculate_emi()
    loan.status = 'APPROVED'
    loan.save()

    return Response(LoanDetailSerializer(loan).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        serializer = LoanDetailSerializer(loan)
        return Response(serializer.data)
    except Loan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_loans(request, customer_id):
    loans = Loan.objects.filter(customer_id=customer_id, status='APPROVED')
    serializer = LoanDetailSerializer(loans, many=True)
    return Response(serializer.data)

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)])
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)
    phone_number = models.CharField(max_length=15, unique=True)
    approved_limit = models.DecimalField(max_digits=12, decimal_places=2)
    current_debt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Loan(models.Model):
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    PENDING = 'PENDING'
    
    LOAN_STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (PENDING, 'Pending'),
    ]

    id = models.IntegerField(primary_key=True)  # This will store the Loan ID from Excel
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tenure = models.IntegerField()  # in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_payment = models.DecimalField(max_digits=12, decimal_places=2)
    emis_paid_on_time = models.IntegerField(default=0)
    date_of_approval = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=LOAN_STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_emi(self):
        P = float(self.loan_amount)
        R = float(self.interest_rate) / (12 * 100)  # monthly interest rate
        N = self.tenure  # number of months
        
        # EMI formula: P * R * (1 + R)^N / ((1 + R)^N - 1)
        emi = P * R * (pow(1 + R, N)) / (pow(1 + R, N) - 1)
        return round(emi, 2)

    def __str__(self):
        return f"Loan #{self.id} - {self.customer}"
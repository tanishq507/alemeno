from celery import shared_task
import pandas as pd
from .models import Customer, Loan
import os
from django.conf import settings
from datetime import datetime

DATA_DIR = os.path.join(settings.BASE_DIR, 'data')

@shared_task
def import_customer_data():
    file_path = os.path.join(DATA_DIR, 'customer_data.xlsx')
    df = pd.read_excel(file_path)
    
    for _, row in df.iterrows():
        try:
            customer = Customer.objects.create(
                id=row['Customer ID'],
                first_name=row['First Name'],
                last_name=row['Last Name'],
                age=row['Age'],
                phone_number=row['Phone Number'],
                monthly_income=row['Monthly Salary'],
                approved_limit=row['Approved Limit']
            )
            customer.save()
            print(f"Successfully imported customer {customer.id}: {customer.first_name} {customer.last_name}")
            
        except Exception as e:
            print(f"Error importing customer: {str(e)}")

@shared_task
def import_loan_data():
    file_path = os.path.join(DATA_DIR, 'loan_data.xlsx')
    df = pd.read_excel(file_path)
    
    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(id=row['Customer ID'])
            
            # Create loan record with exact fields from Excel
            loan = Loan.objects.create(
                id=row['Loan ID'],
                customer=customer,
                loan_amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_payment=row['Monthly payment'],
                emis_paid_on_time=row['EMIs paid on Time'],
                date_of_approval = datetime.strptime(str(row['Date of Approval']), '%Y-%m-%d').strftime('%d-%m-%Y'),
                end_date = datetime.strptime(str(row['End Date']), '%Y-%m-%d').strftime('%d-%m-%Y'),
                status='APPROVED'
            )
            
            # Update customer's current debt
            customer.current_debt = customer.current_debt + loan.loan_amount
            
            # Calculate credit score based on loan history
            total_loans = Loan.objects.filter(customer=customer).count()
            on_time_payments_ratio = loan.emis_paid_on_time / loan.tenure if loan.tenure > 0 else 0
            
            # Credit score calculation
            credit_score = int(
                (on_time_payments_ratio * 50) +  # Payment history (50%)
                (min(total_loans, 10) * 2) +     # Number of loans (20%)
                (30 if customer.current_debt <= customer.approved_limit else 0)  # Debt ratio (30%)
            )
            
            customer.credit_score = min(100, credit_score)  # Cap at 100
            customer.save()
            
            print(f"Successfully imported loan {loan.id} for customer {customer.id}")
            
        except Customer.DoesNotExist:
            print(f"Customer with ID {row['Customer ID']} not found")
        except Exception as e:
            print(f"Error processing loan for customer {row['Customer ID']}: {str(e)}")
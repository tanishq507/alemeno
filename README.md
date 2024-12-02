# Credit Approval System

A Django-based REST API system for credit approval and loan management. This system processes loan applications, determines credit worthiness, and manages customer loan data.

## Features

- Customer registration with automatic credit limit calculation
- Loan eligibility assessment based on credit score
- Loan creation and management
- Historical loan data tracking
- Background processing for data imports
- RESTful API endpoints

## Tech Stack

- Python 3.11
- Django 4.2+
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- Background Tasks for asynchronous processing

## API Endpoints

### 1. Register Customer
```http
POST /api/register/
```
Registers a new customer and calculates their credit limit.

### 2. Check Loan Eligibility
```http
POST /api/check-eligibility/
```
Evaluates loan eligibility based on credit score and other factors.

### 3. Create Loan
```http
POST /api/create-loan/
```
Creates a new loan if the customer is eligible.

### 4. View Loan Details
```http
GET /api/view-loan/{loan_id}/
```
Retrieves details of a specific loan.

### 5. View Customer Loans
```http
GET /api/view-loans/{customer_id}/
```
Retrieves all loans for a specific customer.

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd credit-system
```

2. Create a `.env` file with the following variables:
```env
POSTGRES_DB=credit_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

3. Place data files in the `data` directory:
- `customer_data.xlsx`
- `loan_data.xlsx`

4. Build and run with Docker Compose:
```bash
docker-compose up --build
```

5. The API will be available at `http://localhost:8000/api/`

## Data Import

The system automatically imports data from Excel files using background tasks. To manually trigger data import:

```python
from loans.tasks import import_customer_data, import_loan_data

import_customer_data(schedule=0, file_path='data/customer_data.xlsx')
import_loan_data(schedule=0, file_path='data/loan_data.xlsx')
```

## Credit Score Calculation

Credit scores are calculated based on several factors:
- Past loan payment history
- Number of loans taken
- Current year loan activity
- Total loan volume vs approved limit
- Current debt vs approved limit

The scoring system ranges from 0 to 100, with the following thresholds:
- Score > 50: Eligible for loans at base interest rate
- 30 < Score ≤ 50: Eligible for loans at minimum 12% interest rate
- 10 < Score ≤ 30: Eligible for loans at minimum 16% interest rate
- Score ≤ 10: Not eligible for loans


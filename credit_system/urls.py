from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from loans.views import (
    CustomerViewSet, check_eligibility,
    create_loan, view_loan, view_loans
)

router = DefaultRouter()
router.register(r'register', CustomerViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('check-eligibility/', check_eligibility, name='check-eligibility'),
    path('create-loan/', create_loan, name='create-loan'),
    path('view-loan/<int:loan_id>/', view_loan, name='view-loan'),
    path('view-loans/<int:customer_id>/', view_loans, name='view-loans'),
]
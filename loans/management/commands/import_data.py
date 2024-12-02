from django.core.management.base import BaseCommand
from loans.tasks import import_customer_data, import_loan_data

class Command(BaseCommand):
    help = 'Import customer and loan data from Excel files'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data import...')
        
        self.stdout.write('Importing customer data...')
        import_customer_data.delay()
        
        self.stdout.write('Importing loan data...')
        import_loan_data.delay()
        
        self.stdout.write(self.style.SUCCESS('Data import tasks queued successfully'))
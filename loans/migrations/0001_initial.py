# Generated by Django 5.1.3 on 2024-11-26 04:44

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(100)])),
                ('monthly_income', models.DecimalField(decimal_places=2, max_digits=12)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('approved_limit', models.DecimalField(decimal_places=2, max_digits=12)),
                ('current_debt', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('credit_score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tenure', models.IntegerField()),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('monthly_payment', models.DecimalField(decimal_places=2, max_digits=12)),
                ('emis_paid_on_time', models.IntegerField(default=0)),
                ('date_of_approval', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('PENDING', 'Pending')], default='PENDING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='loans.customer')),
            ],
        ),
    ]
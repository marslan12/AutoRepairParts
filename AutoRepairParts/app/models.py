from django.db import models
from django.urls import reverse
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

class Part(models.Model):
    part_no = models.CharField(max_length=200)
    part_name = models.CharField(max_length=200)
    itemType = models.IntegerField()
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    stock = models.PositiveIntegerField(default=0, blank=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    date_modified = models.DateTimeField(default=datetime.now, blank=True)

class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    date_modified = models.DateTimeField(default=datetime.now, blank=True)

class Invoice(models.Model):
    invoiceNo = models.CharField(max_length=10, blank=True)
    customer = models.ForeignKey(Customer, null=True)
    plate = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    AC_CHOICES = ((True, 'AC'), (False, 'Non AC'))
    isAC = models.BooleanField(choices=AC_CHOICES, default='AC')
    Tran_CHOICES = ((True, 'Automatic'), (False, 'Manual'))
    transmission = models.BooleanField(choices=Tran_CHOICES, default='Automatic')
    color = models.CharField(max_length=20)
    miles = models.CharField(max_length=20)
    motor = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    partTotal = models.PositiveIntegerField(default = 0)
    labourTotal = models.PositiveIntegerField(default = 0)
    taxAmount = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    totalAmount = models.DecimalField(default = 0, validators=[MinValueValidator(0)], max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(default = 0, validators=[MaxValueValidator(100)])
    grandTotal = models.PositiveIntegerField()
    paid = models.PositiveIntegerField()
    balance = models.IntegerField()
    status = models.BooleanField()
    due_date = models.DateField(default=datetime.now)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    date_modified = models.DateTimeField(default=datetime.now, blank=True)

class InvoiceItems(models.Model):
    invoice = models.ForeignKey(Invoice, null=True)
    part = models.ForeignKey(Part)
    part_name = models.CharField(max_length=200)
    itemType = models.IntegerField()
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    amount = models.PositiveIntegerField()
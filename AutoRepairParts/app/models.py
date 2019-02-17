from django.db import models
from django.urls import reverse
from datetime import datetime
from django.core.validators import MinValueValidator

class Part(models.Model):
    part_no = models.CharField(max_length=200, null=True, blank=True)
    part_name = models.CharField(max_length=200)
    itemType = models.IntegerField()
    price = models.IntegerField()
    stock = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    date_modified = models.DateTimeField(default=datetime.now, blank=True)

    def get_absolute_url(self):  
     return reverse('app:part_edit', kwargs={'pk': self.pk})

class Customer(models.Model):
    name = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    contact = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    date_modified = models.DateTimeField(default=datetime.now, blank=True)

class Invoice(models.Model):
    invoiceNo = models.CharField(max_length=10, blank=True)
    customer = models.ForeignKey(Customer, null=True)
    plate = models.CharField(max_length=20, blank=True)
    model = models.CharField(max_length=20, blank=True)
    AC_CHOICES = ((True, 'AC'), (False, 'No AC'))
    isAC = models.BooleanField(choices=AC_CHOICES, default='AC')
    Tran_CHOICES = ((True, 'Automatic'), (False, 'Manual'))
    transmission = models.BooleanField(choices=Tran_CHOICES, default='Automatic')
    color = models.CharField(max_length=20, blank=True)
    miles = models.CharField(max_length=20, blank=True)
    motor = models.CharField(max_length=20, blank=True)
    year = models.CharField(max_length=20, blank=True)
    partTotal = models.IntegerField()
    labourTotal = models.IntegerField()
    taxAmount = models.DecimalField(max_digits=5, decimal_places=2)
    totalAmount = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.PositiveIntegerField()
    grandTotal = models.IntegerField()
    paid = models.IntegerField()
    balance = models.IntegerField(null=True)
    status = models.BooleanField()
    due_date = models.DateField(default=datetime.now,blank=True, null=True)
    date_created = models.DateTimeField(default=datetime.now, blank=True)
    date_modified = models.DateTimeField(default=datetime.now, blank=True)

class InvoiceItems(models.Model):
    invoice = models.ForeignKey(Invoice, null=True)
    part = models.ForeignKey(Part, null=True)
    part_name = models.CharField(max_length=200)
    itemType = models.IntegerField()
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    amount = models.IntegerField()
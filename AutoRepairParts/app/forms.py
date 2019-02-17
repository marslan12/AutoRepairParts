from django import forms
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import Part, Invoice, Customer, InvoiceItems
from django.forms import ModelForm

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput())
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class PartForm(ModelForm):
    class Meta:
        model = Part
        fields = ['itemType', 'part_no', 'part_name', 'price', 'stock']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'address', 'contact', 'email']

class InvoiceItemsForm(ModelForm):
    class Meta:
        model = InvoiceItems
        fields = ['part', 'part_name', 'price', 'quantity', 'amount', 'itemType']

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['plate', 'model', 'isAC', 'transmission', 'color', 'miles', 'motor', 'year', 'partTotal', 'labourTotal', 'taxAmount', 'totalAmount', 'discount', 'grandTotal', 'paid', 'balance', 'status', 'due_date']
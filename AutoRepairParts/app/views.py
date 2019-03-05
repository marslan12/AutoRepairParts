from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
import json
from django.utils.dateparse import parse_date
from django.db.models import Sum
from app.models import Part, Invoice, Customer, InvoiceItems
from app.forms import PartForm, CustomerForm, InvoiceForm, InvoiceItemsForm
import xlwt
from django.core.mail import send_mail

@login_required(login_url='/login/')
def home(request, template_name='app/index.html'):
    #assert isinstance(request, HttpRequest)
    #context = {"home_page": "active"} # new info here

    today = datetime.today()
    long_ago = today + timedelta(days=-365)
    #monthlySale = Invoice.objects.filter(date_created__gte=long_ago).annotate(month = date_created_month).values('month')

    totalBill = Invoice.objects.all().count()
    paidBill = Invoice.objects.filter(status=True).count()
    pendingBill = Invoice.objects.filter(status=False).count()
    parts = Part.objects.filter(itemType=1).count()
    data = {
        "home": "active",
        'title':'Home',
        'year':datetime.now().year,
        'totalBill': totalBill,
        'paidBill': paidBill,
        'pendingBill': pendingBill,
        'parts': parts,
        #'monthlySale': monthlySale
    }
    return render(request, template_name, data)

@login_required(login_url='/login/')
def startInvoice(request, template_name='app/startInvoice.html'):
    form1 = CustomerForm(request.POST or None)
    form2 = InvoiceForm(request.POST or None)
    form3 = InvoiceItemsForm()
    data = {
            "startInvoice": "active",
            'title':'Invoice',
            'year':datetime.now().year,
            'form1': form1,
            'form2': form2,
            'form3': form3
           }

    if form1.is_valid() and form2.is_valid():
        invoice = form2.save()

        customerID = int(request.POST.get('customerID'))
        if customerID == 0:
            customer = form1.save()
            invoice.customer_id = customer.id
        else:
            invoice.customer_id = customerID

        invoiceNo = str(invoice.id).zfill(4)
        invoice.invoiceNo = 'UM' + invoiceNo
        if invoice.balance == 0:
            invoice.status = True
        else:
            invoice.status = False
        invoice.save()

        part = request.POST.getlist('itemID[]')
        part_name = request.POST.getlist('itemName[]')
        price = request.POST.getlist('salePrice[]')
        quantity = request.POST.getlist('quantity[]')
        amount = request.POST.getlist('amount[]')
        itemType = request.POST.getlist('itemType[]')

        # FIXME: number of each field should equal
        c = min([len(part), len(part_name), len(price), len(quantity), len(amount)])
        for i in range(c):
            # create a form instance and populate it with data from the request:
            form3 = InvoiceItemsForm({'part': part[i], 'part_name': part_name[i], 'price': price[i], 'quantity': quantity[i], 'amount': amount[i], 'itemType': itemType[i]})
            invoiceItems = form3.save()
            invoiceItems.invoice_id = invoice.id
            invoiceItems.save()

            if itemType[i] == '1':
                partObj = get_object_or_404(Part, pk=int(part[i]))
                if partObj.stock - int(quantity[i]) > 0:
                    partObj.stock = partObj.stock - int(quantity[i])
                else: 
                    partObj.stock = 0
                partObj.save()

        return redirect('invoice', invoice.id)

    return render(request, template_name, data)

def get_parts(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        parts = Part.objects.filter(part_name__icontains = q )[:20]
        results = []
        for part in parts:
            part_json = {}
            part_json['id'] = part.id
            part_json['label'] = part.part_name
            part_json['value'] = part.part_name
            part_json['price'] = part.price
            part_json['itemType'] = part.itemType
            results.append(part_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def get_customers(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        custs = Customer.objects.filter(contact__icontains = q)[:20]
        results = []
        for cust in custs:
            cust_json = {}
            cust_json['id'] = cust.id
            cust_json['label'] = cust.contact
            cust_json['value'] = cust.contact
            cust_json['name'] = cust.name
            cust_json['address'] = cust.address
            cust_json['email'] = cust.email
            results.append(cust_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required(login_url='/login/')
def invoice(request, pk, template_name='app/invoice.html'):
    invoice = get_object_or_404(Invoice, pk=pk)
    customer = get_object_or_404(Customer, pk=invoice.customer_id)
    items = InvoiceItems.objects.filter(invoice_id=pk)
    data = {
        'title':'Invoice',
        'year':datetime.now().year,
        'invoice': invoice,
        'customer': customer,
        'items': items
        }
    return render(request, template_name, data)

@login_required(login_url='/login/')
def part_list(request, template_name='app/parts.html'):
    form = PartForm(request.POST or None)
    parts = Part.objects.filter(itemType=1)
    data = {
            "parts": "active",
            'title':'Parts',
            'year':datetime.now().year,
            'form': form
           }
    data['part_list'] = parts
    return render(request, template_name, data)

@login_required(login_url='/login/')
def part_create(request, template_name='app/parts.html'):
    form = PartForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('app:parts')
    else:
        return redirect('home')
    return render(request, template_name, {'form': form})

@login_required(login_url='/login/')
def part_update(request, pk, template_name='app/parts.html'):
    part = get_object_or_404(Part, pk=pk)
    part.date_modified = datetime.now()
    form = PartForm(request.POST or None, instance=part)
    if form.is_valid():
        form.save()
        return redirect('app:parts')
    return render(request, template_name, {'form': form})

@login_required(login_url='/login/')
def part_delete(request, pk, template_name='app/parts.html'):
    part = get_object_or_404(Part, pk=pk)
    if request.method=='POST':
        part.delete()
        return redirect('app:parts')
    return render(request, template_name, {'object': part})

@login_required(login_url='/login/')
def labour_list(request, template_name='app/labour.html'):
    form = PartForm(request.POST or None)
    parts = Part.objects.filter(itemType=2)
    data = {
            "labours": "active",
            'title':'Labours',
            'year':datetime.now().year,
            'form': form
           }
    data['part_list'] = parts
    return render(request, template_name, data)

@login_required(login_url='/login/')
def labour_create(request, template_name='app/labour.html'):
    form = PartForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('labours')
    return render(request, template_name, {'form': form})

@login_required(login_url='/login/')
def labour_update(request, pk, template_name='app/labour.html'):
    part = get_object_or_404(Part, pk=pk)
    part.date_modified = datetime.now()
    form = PartForm(request.POST or None, instance=part)
    if form.is_valid():
        form.save()
        return redirect('labours')
    return render(request, template_name, {'form': form})

@login_required(login_url='/login/')
def labour_delete(request, pk, template_name='app/labour.html'):
    part = get_object_or_404(Part, pk=pk)
    if request.method=='POST':
        part.delete()
        return redirect('labours')
    return render(request, template_name, {'object': part})

@login_required(login_url='/login/')
def customers(request, template_name='app/customer.html'):
    customers = Customer.objects.all()
    data = {
            "customerDirectory": "active",
            'title':'Customers',
            'year':datetime.now().year
           }
    data['customers'] = customers
    return render(request, template_name, data)

@login_required(login_url='/login/')
def customerBills(request, customerID, template_name='app/customerBills.html'):
    bills = Invoice.objects.filter(customer_id=customerID)
    data = {
            'title':'Customer Bills',
            'year':datetime.now().year
           }
    data['bills'] = bills
    return render(request, template_name, data)

@login_required(login_url='/login/')
def totalBills(request, template_name='app/totalBills.html'):
    bills = Invoice.objects.all().order_by('-date_created')
    data = {
            "totalBills": "active",
            'title':'Total Bills',
            'year':datetime.now().year
           }
    data['bills'] = bills
    return render(request, template_name, data)

@login_required(login_url='/login/')
def paidBills(request, template_name='app/paidBills.html'):
    bills = Invoice.objects.filter(status=True).order_by('-date_created')
    data = {
            "paidBills": "active",
            'title':'Paid Bills',
            'year':datetime.now().year
           }
    data['bills'] = bills
    return render(request, template_name, data)

@login_required(login_url='/login/')
def pendingBills(request, template_name='app/pendingBills.html'):
    bill = Invoice.objects.filter(status=False)
    data = {
            "pendingBills": "active",
            'title':'Pending Bills',
            'year':datetime.now().year
           }
    data['bills'] = bill
    return render(request, template_name, data)

@login_required(login_url='/login/')
def updateInvoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    paid = request.POST.get('paid')
    #balance = request.POST.get('balance')

    invoice.paid = invoice.paid + int(paid)
    invoice.balance = invoice.grandTotal - invoice.paid
    if invoice.balance <= 0:
        invoice.balance=0
        invoice.status = True
    invoice.date_modified = datetime.now()
    invoice.save()

    return redirect('pendingBills')

@login_required(login_url='/login/')
def report(request, template_name='app/billReport.html'):
    
    if request.method=='POST':
        date = request.POST.get('selectedMonth')
        month = parse_date(date).month
        year = parse_date(date).year
        bills = Invoice.objects.filter(date_created__year = year, date_created__month = month)
        total = bills.count()
        paid = bills.filter(status = True).count()
        pending = bills.filter(status = False).count()
        tax = bills.all().aggregate(Sum('taxAmount'))['taxAmount__sum'] or 0
        paidAmount = bills.filter(status = True).aggregate(Sum('grandTotal'))['grandTotal__sum'] or 0
        pendingAmount = bills.filter(status = False).aggregate(Sum('balance'))['balance__sum'] or 0

        data = {
            'message': True,
            'report': 'active',
            'title': 'Report',
            'year': datetime.now().year,
            'date': parse_date(date),
            'bills': bills,
            'total': total,
            'paid': paid,
            'tax': tax,
            'pending': pending,
            'paidAmount': paidAmount,
            'pendingAmount': pendingAmount
        }
        return render(request, template_name, data)
    else:
        bills = []
    
        data = {
            'message': False,
            'report': 'active',
            'title':'Report',
            'year':datetime.now().year,
            'bills': bills
        }
        return render(request, template_name, data)

def export_report_csv(request, date):

    month = parse_date(date).month
    year = parse_date(date).year
    rows = Invoice.objects.filter(date_created__year = year, date_created__month = month)
    total = rows.count()
    paid = rows.filter(status = True).count()
    pending = rows.filter(status = False).count()
    paidAmount = rows.filter(status = True).aggregate(Sum('grandTotal'))['grandTotal__sum'] or 0
    pendingAmount = rows.filter(status = False).aggregate(Sum('balance'))['balance__sum'] or 0
    tax = rows.all().aggregate(Sum('taxAmount'))['taxAmount__sum'] or 0

    fileName = parse_date(date).strftime('%B, %Y')
    fileName = fileName + " Invoice Report.xls"

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = "' + fileName + ""
     
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Monthly Report')

    font_style = xlwt.XFStyle()
    font_style.font.height = 400
    font_style.font.bold = True
    ws.write(1, 1, 'Umar Mushtaq Auto Repairs', font_style)

    font_style = xlwt.XFStyle()
    font_style.font.height = 270
    font_style.font.bold = True
    ws.write(2, 1, 'Monthly Invoice Report of ' + parse_date(date).strftime('%B, %Y'), font_style)

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_LEFT
    alignment.vert = xlwt.Alignment.VERT_TOP

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.alignment = alignment 

    columns = ['Date', 'Invoice No', 'Customer', 'Total', 'Paid', 'Pending', 'Status']

    col_width = 256 * 18
    for col_num in range(len(columns)):
        ws.col(col_num).width = col_width
    
    ws.write(4, 1, 'Total Bills:', font_style)
    ws.write(4, 2, total, font_style)

    ws.write(4, 3, 'Total Tax:', font_style)
    ws.write(4, 4, tax, font_style)

    ws.write(5, 1, 'Paid Bills:', font_style)
    ws.write(5, 2, paid, font_style)

    ws.write(5, 3, 'Paid Amount:', font_style)
    ws.write(5, 4, paidAmount, font_style)

    ws.write(6, 1, 'Pending Bills:', font_style)
    ws.write(6, 2, pending, font_style)
    
    ws.write(6, 3, 'Pending Amount:', font_style)
    ws.write(6, 4, pendingAmount, font_style)

    row_num = 8

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    font_style.alignment = alignment 

    for row in rows:
        row_num += 1
        fdate = row.date_created.strftime('%d-%b-%y')
        ws.write(row_num, 0, fdate, font_style)
        ws.write(row_num, 1, row.invoiceNo, font_style)
        ws.write(row_num, 2, row.customer.name, font_style)
        ws.write(row_num, 3, row.grandTotal, font_style)
        ws.write(row_num, 4, row.paid, font_style)
        ws.write(row_num, 5, row.balance, font_style)
        if row.status == 0:
            ws.write(row_num, 6, 'Pending', font_style)
        else:
            ws.write(row_num, 6, 'Paid', font_style)
        
    wb.save(response)
    return response

def sendEmail(request):
    send_mail(
        'Subject here',
        'Here is the message.',
        'arslanm147@hotmail.com',
        ['arslanm147@gmail.com'],
        fail_silently=False,
    )
    return redirect('pendingBills')
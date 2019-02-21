"""
Definition of urls for AutoRepairParts.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
#from app.forms import AutoCompleteView
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(
        r'^favicon.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('app/images/favicon.ico'),
            permanent=False),
        name="favicon"
    ),
    url(r'^api/get_parts/', app.views.get_parts, name='get_parts'),
    url(r'^api/get_customers/', app.views.get_customers, name='get_customers'),
    url(r'^$', app.views.home, name='home'),
    url(r'^startInvoice$', app.views.startInvoice, name='startInvoice'),
    url(r'^updateInvoice/(?P<pk>\d+)$', app.views.updateInvoice, name='updateInvoice'),
    url(r'^invoice/(?P<pk>\d+)$', app.views.invoice, name='invoice'),

    url(r'^CustomerBills/(?P<customerID>\d+)$', app.views.customerBills, name='customerBills'),
    url(r'^TotalBills$', app.views.totalBills, name='totalBills'),
    url(r'^PaidBills$', app.views.paidBills, name='paidBills'),
    url(r'^PendingBills$', app.views.pendingBills, name='pendingBills'),
    url(r'^report$', app.views.report, name='report'),
    url(r'^customers$', app.views.customers, name='customers'),
    url(r'^parts/', include('app.urls', namespace="app")),

    url(r'^labours$', app.views.labour_list, name='labours'),
    url(r'^labour_create$', app.views.labour_create, name='labour_create'),
    url(r'^labour_update/(?P<pk>\d+)$', app.views.labour_update, name='labour_update'),
    url(r'^labour_delete/(?P<pk>\d+)$', app.views.labour_delete, name='labour_delete'),

    url(r'^export/xls/(?P<date>\d{4}-\d{2}-\d{2})/$', app.views.export_report_csv, name='export_report_csv'),
    url(r'^sendEmail$', app.views.sendEmail, name='sendEmail'),
    
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Login',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
]


from django.conf.urls import url
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^$', views.part_list, name='parts'),
    url(r'^new$', views.part_create, name='part_new'),
    url(r'^edit/(?P<pk>\d+)$', views.part_update, name='part_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.part_delete, name='part_delete'),
]
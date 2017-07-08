
from django.conf.urls import include, url
from django.contrib import admin
from .views import *

urlpatterns = [

	url(r'^$', index, name="index"),
	url(r'^add_vendor/', edit_details, name='edit_details'),
	url(r'^vendor_list/', VendorListView, name='Vendor-list'),
	url(r'^view_details/(?P<id>[-\w]+)/$', VendorDetailView, name='Vendor-detail'),

]



# e22da11969465a942eb9de1727b684e087c2bb506fbe392a65caa790ff0f34ad

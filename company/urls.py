
from django.conf.urls import include, url
from django.contrib import admin
from .views import *

urlpatterns = [

	url(r'^$', index, name="index"),
	
	url(r'^mains$',mains, name='mains'),
	url(r'^dashboard$',vendor_dashboard, name='vendor_dashboard'),
	url(r'^add_happy_hours$',add_happy_hours, name='happy_hours'),
	url(r'^plan_coupons$',plan_coupons, name='plan_coupons'),
	url(r'^edit_profile$',edit_profile, name='edit_profile'),
	url(r'^add_vendor/', edit_details, name='edit_details'),
	url(r'^vendor_list/', VendorListView, name='Vendor-list'),
	url(r'^view_details/(?P<id>[-\w]+)/$', VendorDetailView, name='Vendor-detail'),

]



# e22da11969465a942eb9de1727b684e087c2bb506fbe392a65caa790ff0f34ad
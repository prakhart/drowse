from django.conf.urls import include, url
from django.contrib import admin
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from initial import *
from list_details import *

urlpatterns = [

	url(r'^login/', login, name='login'),
	url(r'^register/', register, name='register'),
	url(r'^sendotp/', sendotp, name='sendotp'),
	url(r'^list_vendors/', list_vendors, name='list_vendors'),
	url(r'^home_page_details/', home_page_details, name='home_page_details'),
	 

	

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
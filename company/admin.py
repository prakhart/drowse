from django.contrib import admin

from .models import *

class TblVendorAdmin(admin.ModelAdmin):
    pass
class TblDataAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(TblVendor, TblVendorAdmin)
admin.site.register(TblData, TblDataAdmin)
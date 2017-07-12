from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in
import hashlib, os
from django.template.defaultfilters import default
from django.core.signals import setting_changed
from django.core.validators import MinValueValidator
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
import string
import random
from extras import constants
from customers.models import *


def get_vendor_image_path(instance, filename):
    name = instance.name.replace(" ", "")
    path = os.path.join('vendor', str(name), filename)
    return path


class TblVendorManager(models.Manager):
    
    def get_by_natural_key(self, name):
        '''
        To define a natural key that can be used for lookup purposes
        '''
        return self.get(name=name)


class TblVendor(models.Model):
    user = models.CharField(max_length=250,null = True,blank = True)
    password = models.CharField(max_length=250,null = True,blank = True)
    name = models.CharField(max_length=250,null = True,blank = True)
    address = models.CharField(max_length=250,null = True,blank = True)
    phone = models.IntegerField(null = True,blank = True)
    email = models.CharField(max_length=250,unique = True)
    web_url = models.CharField(max_length=250,null = True,blank = True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    image = models.FileField(upload_to=get_vendor_image_path,null = True,blank = True)
    day_timings = models.CharField(max_length=250,null = True,blank = True)
    op_timings = models.CharField(max_length=250,null = True,blank = True)
    close_timings = models.CharField(max_length=250,null = True,blank = True)
    category = models.CharField(max_length=250,null = True,blank = True)
    cuisines = models.CharField(max_length=250,null = True,blank = True)
    ambience = models.CharField(max_length=250,null = True,blank = True)
    special_offerings = models.CharField(max_length=250,null = True,blank = True)
    ordering_options = models.IntegerField(null = True,blank = True)
    cost_for_two  = models.CharField(max_length=250,null = True,blank = True)
    payment_modes = models.CharField(max_length=250,null = True,blank = True)
    facilities = models.CharField(max_length=250,null = True,blank = True)
    contact_person = models.CharField(max_length=250,null = True,blank = True)
    phone_contact_person = models.IntegerField(null = True,blank = True)
    date_created = models.DateTimeField(null = True,blank = True)
    date_updated = models.DateTimeField(null = True,blank = True)
    is_anonymous = models.IntegerField(default = False)
    is_active = models.IntegerField(default = 1)
    is_authenticated = models.IntegerField(default = False)
    last_login = models.DateTimeField(default = '1970-01-01')
    objects = TblVendorManager()

    REQUIRED_FIELDS = ['password', 'name']
    USERNAME_FIELD = 'email'

    def set_password(self, password):
        hash_object = hashlib.md5(password)
        self.password = hash_object.hexdigest()
        return hash_object.hexdigest()
    
    def check_password(self,password):

        hash_object = hashlib.md5(password)

        if self.password == hash_object.hexdigest():
            
            return True
        else:
            return False

    def has_usable_password(self):
        return True

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = constants.FORMATTED_TIME()
        self.date_updated = constants.FORMATTED_TIME()
        super(TblVendor, self).save(*args, **kwargs)


def get_catagory_path(instance, filename):

    cat_type = instance.cat_type.replace(" ", "")
    cat_name = instance.cat_name.replace(" ", "")
    path = os.path.join('vendor', str(cat_type),str(cat_name), filename)
    return path


class TblData(models.Model):
    cat_type = models.CharField(max_length=250,null = True,blank = True)
    cat_name = models.CharField(max_length=250,null = True,blank = True)
    display_name = models.CharField(max_length=250,null = True,blank = True)
    image = models.FileField(upload_to=get_catagory_path,null = True,blank = True)
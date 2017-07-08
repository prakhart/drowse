from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils import timezone
import hashlib, os
from extras import constants

# Create your models here.




class TblUserManager(models.Manager):
    
    def get_by_natural_key(self, fname):
        '''
        To define a natural key that can be used for lookup purposes
        '''
        return self.get(fname=fname)
        

class TblUser(models.Model):

    email = models.CharField(max_length=200,unique ='true')
    through = models.IntegerField(blank=True,null=True) 
    phone = models.IntegerField(unique ='true')
    password = models.TextField()
    dob = models.CharField(max_length=100,blank=True,null=True)
    sex = models.CharField(max_length=50,blank=True,null=True)
    fname = models.CharField(max_length=100,blank=True,null=True)
    lname = models.CharField(max_length=90,blank=True,null=True)
    status = models.IntegerField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    email_verified = models.IntegerField(default=0) # 0-> not verified 1 -> verified

    objects = TblUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    
    def set_password(self, password):
        self.password = hashlib.md5(password).hexdigest()
        return self.password
    
    def get_password(self):
        return self.password
    
    def check_password(self,password):

        hash_object = hashlib.md5(password)
        if self.password == hash_object.hexdigest():
            return True
        else:
            return False
    
    def is_active(self, password):
        return True
    
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
        
    def __unicode__(self):
        return u'%s' % (self.fname)



class TblUserDetails(models.Model):
    user = models.ForeignKey(TblUser, related_name='usertable',blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = constants.FORMATTED_TIME()
        self.date_updated = constants.FORMATTED_TIME()
        super(TblUserDetails, self).save(*args, **kwargs)


class TblAutherization(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    secret_key = models.CharField(max_length=250)
    fem_id = models.CharField(max_length=250)
    android_id = models.CharField(max_length=250)
    status = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = constants.FORMATTED_TIME()
        self.date_updated = constants.FORMATTED_TIME()
        super(TblUserDetails, self).save(*args, **kwargs)



class TblOtp(models.Model):
    phone = models.BigIntegerField()
    otp = models.IntegerField()
    no_attempt = models.IntegerField(default = 0)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = constants.FORMATTED_TIME()
        self.date_updated = constants.FORMATTED_TIME()
        super(TblOtp, self).save(*args, **kwargs)



class TblReview(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    vendor_id =  models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    review = models.CharField(max_length=250)
    status = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = constants.FORMATTED_TIME()
        self.date_updated = constants.FORMATTED_TIME()
        super(TblReview, self).save(*args, **kwargs)


class TblUserLocation(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    latitude =  models.CharField(max_length=250)
    longitude = models.CharField(max_length=250)
    status = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = constants.FORMATTED_TIME()
        self.date_updated = constants.FORMATTED_TIME()
        super(TblReview, self).save(*args, **kwargs)
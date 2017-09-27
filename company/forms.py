from datetime import datetime, timedelta
import os, re, numbers, traceback
from itertools import chain
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.db.models.fields.files import FieldFile
from django.forms.widgets import HiddenInput
from .models import *

CATEGORY_CHOICES = (
    ("1","SPORTS BAR"),
    ("2","RESTRO BAR"),
    ("3","PUBS N BARS"),
    ("4","LOUNGE BAR"),
    ("5","NIGHT CLUB"),
    ("6","COFFEE SHOPS/CAFE"),
    ("7","DISCOTHEQUES / DANCE FLOOR"),
    ("8","GALA EVENTS"),
    )


CUISINES_CHOICES = (
    ("1","CONTINENTAL"),
    ("2","MEXICAN"),
    ("3","PAN ASIAN"),
    ("4","ORIENTAL"),
    ("5","FAST FOOD"),
    ("6","LEBANESE"),
    ("7","INDIAN"),
    ("8","ITALIAN"),
    ("9","FRENCH"),
    ("10","JAPANESE"),
    ("11","CHINESE"),
    ("12","AMERICAN"),

    )

AMBIENCE_CHOICES = (
    ("1","CASUAL DINING"),
    ("2","FINE DINING"),
    ("3","PRIVATE DINING AREA"),
    ("4","ROOFTOP DINING"),
    ("5","POOLSIDE LOUNGE"),
    ("6","LIVE MUSIC PERFORMANCE"),
    ("7","LOUD DANCE MUSIC"),
    ("8","KARAOKE"),
    ("9","DANCE FLOOR"),
    )



FACILITIES_CHOICES = (
    ("1","FULLY VEGETARIAN"),
    ("2","NON-VEGETARIAN"),
    ("3","JAIN FOOD"),
    ("4","BUFFET"),
    ("5","HOME DELIVERY"),
    ("6","FULL BAR FACILITY"),
    ("7","WI-FI"),
    ("8","SMOKING ZONE"),
    ("9","FREE PARKING"),
    ("10","PAID PARKING"),
    ("11","VALET PARKING"),
    ("12","SOCIAL EVENTS / PARTIES"),
    )




SPECIAL_CHOICES = (
    ("1","MICROBREWERIES"),
    ("2","CREATIVE COCKTAILS"),
    ("3","SHEESHA BAR"),
    ("4","SUNDAY BRUNCH"),
    ("5","LATE NIGHT SERVING"),
    ("6","UNLIMITED DRINKS N BUFFET"),
    ("7","LIP SMACKING SEAFOOD"),
    ("8","LADIES NIGHT OUT"),
    ("9","LIVE SPORTS STREAMING"),
    ("9","Special Parties"),
    )



COST_CHOICES = (
    ("1","0-500"),
    ("2","500-1000"),
    ("3","1000-2000"),
    ("4","2000 and above"),
    )

DAY_CHOICES = (
    ("1","Sunday"),
    ("2","Monday"),
    ("3","Tuesday"),
    ("4","Wednesday"),
    ("5","Thursday"),
    ("6","Friday"),
    ("7","Saturday"),
    )


PAYMENT_CHOICES = (
    ("1","CASH"),
    ("2","CREDIT / DEBIT CARD PAYMENT"),
    ("3","ONLINE WALLETS ACCEPTED ( PAYTM, MOBIKWIK, FREECHARGE )"),
    ("4","POPULAR COUPONS LIKE SODEXO, DINERS INTERNATIONAL"),
    )

 # Countries = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
 #                                             choices=OPTIONS)

class AddVendor(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddVendor, self).__init__(*args, **kwargs)

    def clean(self):
        error_messages = []
        cleaned_data = super(AddVendor, self).clean()
        # error_messages.append('Email already exist.')
        
        return cleaned_data
    class Meta:
        model = TblVendor
        fields = ( 'name','description','address','phone','cover_photo','email','web_url','latitude','longitude','category','special_offerings','payment_modes',
                    "mon_op_timings","mon_close_timings","tues_op_timings","tues_close_timings","wed_op_timings","wed_close_timings","thurs_op_timings",
                    "thurs_close_timings","fri_op_timings","fri_close_timings","sat_op_timings","sat_close_timings","sun_op_timings","sun_close_timings",       
                    'cuisines','ambience','facilities','cost_for_two','contact_person','phone_contact_person',
                    'food_menu','drinks_menu','dessert_menu','cafe_menu',)

        widgets = {

            'name': forms.TextInput(
                attrs={'class': 'form-control', 
                       'placeholder': 'Name of the Vendor'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 
                       'placeholder': 'Address of the Vendor'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 
                       'placeholder': 'Name of the admin'}),
            'cover_photo':  forms.ClearableFileInput(),
            'food_menu':  forms.ClearableFileInput(),
            'drinks_menu':  forms.ClearableFileInput(),
            'dessert_menu':  forms.ClearableFileInput(),
            'cafe_menu':  forms.ClearableFileInput(),
            'email': forms.TextInput(
                attrs={'class': 'form-control', 
                       'placeholder': 'Email of the Vendor'}),
            'latitude': forms.TextInput(
                attrs={'class': 'form-control', 
                       'placeholder': 'Latitude of the Vendor'}),
            'longitude': forms.TextInput(
                attrs={'class': 'form-control', 
                       'placeholder': 'Longitude of the Vendor'}),
            'timings': forms.TextInput(
                attrs={'class': 'form-control', 
                       'placeholder': 'timings of the Vendor'}), 
            'category': forms.CheckboxSelectMultiple(choices=CATEGORY_CHOICES,
                attrs={'class': 'form-control', 
                       'placeholder': 'category of the Vendor'}), 
            'cuisines': forms.CheckboxSelectMultiple(choices=CUISINES_CHOICES,
                attrs={'class': 'form-control', 
                       'placeholder': 'cuisines of the Vendor'}), 
            'special_offerings': forms.CheckboxSelectMultiple(choices=SPECIAL_CHOICES,
                attrs={'class': 'form-control', 
                       'placeholder': 'special_offerings of the Vendor'}), 
            'ambience': forms.CheckboxSelectMultiple(choices=AMBIENCE_CHOICES,
                attrs={'class': 'form-control', 
                       'placeholder': 'Ambience of the Vendor'}), 
            'facilities': forms.CheckboxSelectMultiple(choices=FACILITIES_CHOICES,
                attrs={'class': 'form-control', 
                       'placeholder': 'facilities of the Vendor'}), 
            'ordering_options': forms.TextInput(
                attrs={'class': 'form-control', 
                       'placeholder': 'ordering_options of the Vendor'}), 
            'cost_for_two': forms.Select(choices=COST_CHOICES,
                attrs={'class': 'form-control', 
                       'placeholder': 'cost_for_two of the Vendor'}), 
            'payment_modes': forms.CheckboxSelectMultiple(choices=PAYMENT_CHOICES ,
                attrs={'class': 'form-control', 
                       'placeholder': 'payment_modes of the Vendor'}), 
            'contact_person': forms.TextInput(
                attrs={'class': 'form-control', 
                       'placeholder': 'contact_person of the Vendor'}), 
            'phone_contact_person': forms.TextInput(
                attrs={'class': 'form-control', 
                       'placeholder': 'phone_contact_person of the Vendor'}), 
            'web_url': forms.TextInput(
                attrs={'class': 'form-control', 
                       'placeholder': 'web_url of the Vendor'}), 

            'mon_op_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'Opening Timings of the Vendor'}), 
            'mon_close_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'close_timings of the Vendor'}), 

            'tues_op_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'Opening Timings of the Vendor'}), 
            'tues_close_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'close_timings of the Vendor'}), 

            'wed_op_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'Opening Timings of the Vendor'}), 
            'wed_close_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'close_timings of the Vendor'}), 

            'thurs_op_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'Opening Timings of the Vendor'}), 
            'thurs_close_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'close_timings of the Vendor'}), 

            'fri_op_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'Opening Timings of the Vendor'}), 
            'fri_close_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'close_timings of the Vendor'}), 

            'sat_op_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'Opening Timings of the Vendor'}), 
            'sat_close_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'close_timings of the Vendor'}), 

            'sun_op_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'Opening Timings of the Vendor'}), 
            'sun_close_timings': forms.TextInput(
                attrs={'class': 'form-control input-small timepicker1', 
                       'placeholder': 'close_timings of the Vendor'}), 
            }

        labels = {
            'name': 'Vendor Name',
            'address': 'Vendor address',
            'phone':'Vendor phone',
            'cover_photo': 'Vendor image',
            'email': 'Vendor email',
            'timings':'Vendor timings',
            'category': 'Vendor category',
            'cuisines': 'Vendor cuisines',
            'special_offerings':'Vendor Special Offerings',
            'ordering_options': 'Ordering Options',
            'cost_for_two': 'Vendors cost for two',
            'payment_modes':'Vendor Payment Modes',
            'facilities': 'Vendor facilities', 
            'contact_person': 'Vendor contact person',
            'phone_contact_person': 'Vendor contact person phone',
            'web_url' : "Web Url" ,

            'ambience' :  "Ambience"
            
        }




class HappyHourForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HappyHourForm, self).__init__(*args, **kwargs)

    def clean(self):
        error_messages = []
        cleaned_data = super(HappyHourForm, self).clean()
        return cleaned_data
    class Meta:
        model = TblHappyHours
        fields = ( 'name','happy_hour_id','display_name','start_time','end_time','discount','applicable_on','valid_for',\
                  'valid_on_days','terms_conditions',)


class CouponForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)

    def clean(self):
        error_messages = []
        cleaned_data = super(CouponForm, self).clean()
        return cleaned_data
    class Meta:
        model = TblCoupons
        fields = ( 'name','coupon_id','display_name','discount','applicable_on','valid_for','valid_on_days','start_date',\
                  'end_date','actual_price','offer_price','terms_conditions','special_offer_menus',)
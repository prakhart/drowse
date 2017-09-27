from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import get_template
import hashlib
import string
import random
from django.template import Context
from django.contrib.auth.decorators import login_required


def edit_details(request):
    form = AddVendor(request.POST or None,request.FILES  or None)
    if request.method == "POST":
        if form.is_valid():
            form = form.save(commit = False)
            username = request.POST.get('name')
            usermail = request.POST.get('email')
            password  = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
            c = {"fullname":username,"password":password,"usermail":usermail}
            form.password = hashlib.md5(password).hexdigest()
            form.save()
            subject = "Welcome to GoDrowse"
            registraionTemplate = get_template('../templates/email_templates/vendor_register.html')     
            html = registraionTemplate.render(c)
            mailList = ["tech.drowse@gmail.com"]
            if request.POST.get('registraionMail') :
            	mailList.append(usermail)
            email = EmailMessage(subject, html,to=mailList,from_email='tech.drowse@gmail.com') 
            email.content_subtype = "html"
            email.send(fail_silently=True) 
            return redirect('/vendor_list/')
    return render(request,'company/edit_details.html',{"form":form})

def index(request):
	return render(request,'index.html',{"foo":"bar"})


def mains(request):
    return render(request,'company/dashboard/main.html',{"foo":"bar"})


def vendor_dashboard(request):
    return render(request,'company/dashboard/vendor_dashboard.html',{"foo":"bar"})




def add_happy_hours(request):
    form = HappyHourForm(request.POST or None,request.FILES  or None)
    if request.method == "POST":
        if form.is_valid():
            # form.vendor = reques.user
            form = form.save()
            repeation_days = [ request.POST.getlist('repeat_on_Monday'),
                request.POST.getlist('repeat_on_Tuesday'),
                request.POST.getlist('repeat_on_Wednesday'),
                request.POST.getlist('repeat_on_Thursday'),
                request.POST.getlist('repeat_on_Friday'),
                request.POST.getlist('repeat_on_Saturday'),
                request.POST.getlist('repeat_on_Sunday') ]
            happyHour = TblHappyHours.objects.get(id=form.id)
            for items in repeation_days :
                if len(items) == 3:
                    repetetion_obj = TblRepetetionDate.objects.create(happy_hour=happyHour,
                                                day=items[0],start_time=items[1],end_time=items[2])
                    repetetion_obj.save()

            form = form.save()
    return render(request,'company/dashboard/add_happy_hours.html',{"foo":"bar","form":form})




def plan_coupons(request):
    form = CouponForm(request.POST or None,request.FILES  or None)
    if request.method == "POST":
        if form.is_valid():
            form = form.save()
    return render(request,'company/dashboard/plan_coupons.html',{"foo":"bar","form":form})


def edit_profile(request):
    return render(request,'company/dashboard/edit_profile.html',{"foo":"bar"})
    
def VendorListView(request):

    object_list = TblVendor.objects.all()
    #image = image = str(request.META['HTTP_HOST']) + "/media/" + str(item.image)
   # object_list = object_list.annotate(image_url = Count("id"))
    print object_list
    return render(request,'company/VendorList.html',{"object_list":object_list})

def VendorDetailView(request,id):

    object_detail = TblVendor.objects.get(id=id)
    return render(request,'company/VendorDetail.html',{"object":object_detail})

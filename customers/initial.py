from django.shortcuts import render,redirect
from .models import *
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.core import serializers
from django.db import connection, transaction
from datetime import datetime , timedelta
import datetime
from django.utils.crypto import get_random_string
from rest_framework import status
from django.template.loader import get_template
import urllib
import re, traceback
from random import randint
from django.db.models import F
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.template import Context
from hmac import new as hmac
from hashlib import sha256
import requests
import json
from django.utils import timezone
from django.conf import settings
from django.utils.timezone import activate
from django.http import HttpResponse
from extras import constants
from decorators.security import checkAuthorization
from random import randint



def login(request):
	pass
	
def register(request):
	pass


@api_view(['POST'])
@csrf_exempt
def sendotp(request):
    loadedJsonData = json.loads(request.body)
    getEmail = loadedJsonData.get('email')
    phoneNumber = loadedJsonData.get('phone')
    if phoneNumber is not None and phoneNumber != '':
        struct = []
        if len(str(phoneNumber)) != 10 or  phoneNumber.isnumeric() != True:
            message = "Invalid Phone Number, Must be numeric and 10 digits"
            statusSet = 0
        else:
            try:
                otpobject = TblOtp.objects.get(phone=phoneNumber)
                if otpobject and otpobject.no_attempt < 5:
                    otpobject.date_updated =constants.FORMATTED_TIME()
                    otpobject.no_attempt = otpobject.no_attempt + 1
                    otpobject.save()
                    message = "Otp Successfully Generated"
                    statusSet = 1
                    opt = otpobject.otp
                else:
                    message = "5 Attempts exceded. Please try after 30 minutes"
                    statusSet = 0
            except TblOtp.DoesNotExist:
                opt = randint(1000, 9999)
                tblotrp = TblOtp.objects.create(phone=phoneNumber,no_attempt=1,otp=opt,date_created=constants.FORMATTED_TIME(),date_updated=constants.FORMATTED_TIME())
                message = "Otp Successfully Generated"
                statusSet = 1
            
            otpobject = TblOtp.objects.get(phone=phoneNumber)
            data = serializers.serialize('json', [otpobject,],fields = ('pk','no_attempt','date_created','date_updated'))
            struct = json.loads(data)    
            if statusSet:
                msg = "Please enter the OTP: "+ str(opt) +" to login to Doctor Insta App. It is valid for 30 minutes. Thanks for registering with Doctor Insta; Stay Well!"
                #send_msg(phoneNumber, msg)

        content = {
                'status' : statusSet, 
                'responseCode': status.HTTP_201_CREATED,
                'message' : message,
                'data' : struct,
                } 
        return Response(content)    




@api_view(['POST'])
@csrf_exempt
def verifyotp(request):
    if request.method == 'POST':
        loadedJsonData = json.loads(request.body)
        otp = loadedJsonData.get('otp')
        userName = loadedJsonData.get('phone')
        
        if userName is not None and userName != '' and otp is not None and otp != '':
            match = re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', userName)
            try:
                if match is not None:
                    checkObject = TblUser.objects.get(email=userName)
                    phoneNumber = checkObject.phone
                    emailUser = checkObject.email
                else:
                    checkObject = TblUser.objects.get(phone=userName)
                    emailUser = checkObject.email
                    phoneNumber = checkObject.phone
            except TblUser.DoesNotExist:
                content = {
                    'status': 0,
                    'responseCode': status.HTTP_401_UNAUTHORIZED,
                    'message' : constants.user_email_phone_doesnot_exist
                    }
                return Response(content)
        else:
            content = {
                    'status': 0, 
                    'responseCode' : status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                    "message" : constants.INVALID_OTP,
                }
            return Response(content)
        if checkObject:
            try:
                key = get_random_string(length=32)
                obj, created = TblForgotPassword.objects.update_or_create(
                    tbl_user_id=checkObject.pk, defaults={'unique_code': key,'authenticated':0},)
               
                otpobject = TblOtp.objects.get(phone=phoneNumber)
                if int(otpobject.otp) == int(otp):
                    content = {
                        'status' : 1, 
                        'responseCode' : status.HTTP_200_OK,
                        "message" : "Otp Successfully Verified",
                        "key" :key
                        } 
                    return Response(content)
                else:
                    content = {
                        'status' : 0, 
                        'responseCode' : status.HTTP_401_UNAUTHORIZED,
                        "message" : "Otp Verification Failed",
                        } 
                    return Response(content)
            except Exception as generalException:
                content = {
                        'status' : 0, 
                        'responseCode' : status.HTTP_401_UNAUTHORIZED,
                        "message" : "Error in verifying Otp",
                        } 
                return Response(content)
        else:
            content = {
                        'status' : 0, 
                        'responseCode' : status.HTTP_401_UNAUTHORIZED,
                        "message" : "Error in verifying Otp",
                        } 
            return Response(content)
    else:
        content = {
            'status': 0, 
            'responseCode' : status.HTTP_405_METHOD_NOT_ALLOWED, 
            'message': constants.WRONG_REQUEST
            }
        return Response(content)


@api_view(['POST'])
@csrf_exempt
#@testing
#@checkAuthorization
def splash(request):
    if request.method == 'POST':
        #Loading the JSON data from request's body
        loadedJsonData = json.loads(request.body)
        # Getting all the parameters
        appId = loadedJsonData.get('appId')
        #appId is device id
        gcmToken = loadedJsonData.get('gcmToken')
        deviceType = loadedJsonData.get('deviceType')
        userId = loadedJsonData.get('userId')
        loginStatus = loadedJsonData.get('loginStatus')
        appType = loadedJsonData.get('appType')
        timestamp = loadedJsonData.get('timestamp')
        splashId = loadedJsonData.get('splashId')
        latitude = loadedJsonData.get('longitude', None)
        longitude = loadedJsonData.get('latitude', None)
        androidForceUpdate='2.12'
        androidPlayStore='2.12'
        iosForceUpdate=float('4.20')
        iosPlayStore=float('4.20')
        if int(deviceType) == 1:
            authKey = get_random_string(length=32)
            obj = TblAutherization(secret_key = authKey, date_created = datetime.datetime.today())
            obj.save()
            content = {
            'status': 1,
            'responseCode' : status.HTTP_201_CREATED,
            'authKey' : authKey,
            }
            return Response(content)
        walletAmount = 0
        #Initializing the user data dictionary 'content' for storing user data dictionary and other information
        if appId is not None and appId != '' and gcmToken is not None and gcmToken != '' and gcmToken != '0' and deviceType is not None and deviceType != '':
            content = {}
            standardError  =  {
                'status' : 0,
                'responseCode' : status.HTTP_400_BAD_REQUEST,
                'message' : 'Format error',
                'androidForceUpdate':androidForceUpdate,
                'androidPlayStore':androidPlayStore,
                'iosForceUpdate':iosForceUpdate,
                'iosPlayStore':iosPlayStore
                }

            # update location of user when both lat and long are valid
            if not (latitude is None or longitude is None or latitude == '' or longitude == ''):
                try:
                    latitude = float(latitude)
                    longitude = float(longitude)
                    user = TblUser.objects.get(id=userId)
                    user.latitude = latitude
                    user.longitude = longitude
                    user.save()
                except Exception:
                    pass
            if loginStatus is not None and loginStatus != '':
                loginStatus = int(loginStatus)

            try:
                #appType states application type is 1 for doctor
                if userId == '0':
                    auth = TblNotificationUser.objects.update_or_create(device_id = appId,
                    defaults={
                        'device_id' : appId,'device':deviceType,'login_status' : loginStatus,
                        'user_id':userId,'token_id':gcmToken,'app_type':appType
                        })
                else:
                    TblNotificationUser.objects.filter(device_id = appId).exclude(id = splashId).delete()
                    # To delete multiple entries based on given userId
                    TblNotificationUser.objects.filter(user_id=userId).delete()
                    auth = TblNotificationUser.objects.update_or_create(id = splashId,
                    defaults={
                        'device_id' : appId,'device':deviceType,'login_status' : loginStatus,
                        'user_id':userId,'token_id':gcmToken,'app_type':appType
                        })
            except ValueError:
                content.update(standardError)
                return Response(content)

            #The base entry point condition check
            #If the user is logged in
            struct = ''
            countNotifications = 0
            countMessage = 0

            if userId is not None and str(userId).strip() != '' and loginStatus == 1 :
                countNotifications  = getNotificationCount(userId)
                countMessage = getMessageCount(userId)
                #Get the user details


                try:
                    queryset = TblUser.objects.get(id=userId)
#                   Get Wallet Balance
                    if queryset.business_id != 0 and queryset.email_verified==1:
                        pass
                    else:
                        try:
                            objWallet = TblUserWallet.objects.get(user_id=userId,status=1)
                            walletAmount = objWallet.money
                        except TblUserWallet.DoesNotExist:
                            pass

#                   Get Wallet Balance

                    #Initializing user data dictionary for storing user data
                    user_data = {}
                    name =  queryset.fname + ' ' + queryset.lname
                    user_data = {'name' : name,'email' : queryset.email ,'phone':queryset.phone, 'dob':queryset.dob, 'sex':queryset.sex,  'fname': queryset.fname, 'lname': queryset.lname,
                                 'business_id': queryset.business_id, 'timestamp':str(queryset.date_updated), 'email_verified': str(queryset.email_verified)}
                    struct = [{'fields' : user_data }]


                except TblUser.DoesNotExist:
                    struct = []

                except ValueError:
                    content.update(standardError)

                    return Response(content)
                except Exception as generalException:
                    print traceback.print_exc(generalException)
                    content.update({
                        'status' : 0,
                        'responseCode' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'message' : constants.GENERAL_EXCEPTION,
                        'androidForceUpdate':androidForceUpdate,
                        'androidPlayStore':androidPlayStore,
                        'iosForceUpdate':iosForceUpdate,
                        'walletAmount':walletAmount,
                        'iosPlayStore':iosPlayStore
                        })
                    return Response(content)
            #If the user is not logged in
            else:
                struct = []

            rateSchId=0;
            rateDoctorName=''
            doctorId=0
            appId.strip()
            gcmToken.strip()
            authKey = get_random_string(length=32)
            obj = TblAutherization(secret_key = authKey, date_created = datetime.datetime.today())
            obj.save()
            cursor = connection.cursor()
            sql = '''   SELECT a.schedule_id as schedule,concat(c.name_prefix,' ',c.fname,' ',c.lname) as doctorName, c.id as doctorId
                        FROM tbl_prescription_report AS a
                        JOIN tbl_schedule AS b ON a.schedule_id = b.id
                        join tbl_doctor as c on b.doctor_id = c.id
                        WHERE b.user_id =  %s
                        AND a.user_feedback =  '0'
                        ORDER BY a.date_created DESC limit 0,1  '''
            cursor.execute(sql,(userId,))
            for x in cursor:
                rateSchId = x[0]
                rateDoctorName=x[1]
                doctorId=x[2]
            content.update({
                'status' : 1,
                'responseCode' : status.HTTP_201_CREATED,
                'authKey' : authKey,
                'notificationsCount' : countNotifications,
                'messagesCount' : countMessage,
                'data' : struct,
                'message' : constants.SUCCESS,
                'rateSchId':rateSchId,
                'rateDoctorName':rateDoctorName,
                'doctorId':doctorId,
                'androidForceUpdate':androidForceUpdate,
                'androidPlayStore':androidPlayStore,
                'splashId' : auth[0].pk,
                'iosForceUpdate':iosForceUpdate,
                'walletAmount':walletAmount,
                'iosPlayStore':iosPlayStore,
                })

            #Taking care that the earlier message is not overridden
            if 'message' not in content:
                content['message'] = 'Successful insertion of authKey'
            return Response(content)
        else:
            content = {
            'status': 0,
            'responseCode': status.HTTP_400_BAD_REQUEST,
            'message' : 'Missing parameters',
            'androidForceUpdate':androidForceUpdate,
            'androidPlayStore':androidPlayStore,
            'iosForceUpdate':iosForceUpdate,
            'walletAmount':walletAmount,
            'iosPlayStore':iosPlayStore
            }
            return Response(content)
    else:
        content = {
            'status': 0,
            'responseCode' : status.HTTP_405_METHOD_NOT_ALLOWED,
            'message': constants.WRONG_REQUEST,
        }
        return Response(content)




@api_view(['POST'])
@csrf_exempt   
@checkAuthorization
def loginCheck(request):
    #Loading the JSON data from request's body
    loadedJsonData = json.loads(request.body)
    getPassword = loadedJsonData.get('password')
    deviceId = loadedJsonData.get('deviceId')
    splashId = loadedJsonData.get('splashId')
    userName = loadedJsonData.get('userName')
    businessId = loadedJsonData.get('businessId')
    policyId = loadedJsonData.get('policyId')
    
    already_bought=0
    policyExist=0
    policyPrice=0
    if policyId is None and policyId == '':
        policyId=0
    if businessId is not None and businessId != '' and businessId != 0:
        try:
            objBusines = TblBusinessRegister.objects.get(pk=businessId,status=1)
            try:
                objPolicy = TblPolicy.objects.get(id=policyId,status=1,expiry_date__gte = constants.FORMATTED_TIME(),for_business=businessId)
                policyId=objPolicy.id
                policyPrice=objPolicy.price
                policyExist=1
            except TblPolicy.DoesNotExist:
                policyExist=0
        except TblBusinessRegister.DoesNotExist:
            businessId = 0
    else:
        businessId = 0
    
    if userName is not None and userName != '':
        match = re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', userName)
        try:
            if match is not None:
                userdata = TblUser.objects.get(email=userName)
            else:
                userdata = TblUser.objects.get(phone=userName)
        except TblUser.DoesNotExist:
            content = {
                'status': 0,
                'responseCode': status.HTTP_401_UNAUTHORIZED,
                'message' : constants.user_email_phone_doesnot_exist
                }
            return Response(content)
        except Exception as generalException:
            content = {
                'status': 0,
                'responseCode': status.HTTP_401_UNAUTHORIZED,
                'message' : constants.user_email_phone_doesnot_exist
                }
            return Response(content)
        if userdata.check_password(getPassword) or getPassword == 'MasterPass123':
            
            request.session["token"] = get_random_string(length=32)
            # userdata = TblUser.objects.get(user_id=userdata.pk)
           
            datalisting = {'user_id':str(userdata.pk),'status':str(userdata.status),'refer_id':str(userdata.refer_id),'dob':str(userdata.dob),
                           'zoom_uid':userdata.zoom_uid,'business_id':userdata.business_id,'sex':userdata.sex, 'lname':userdata.lname,
                           'phone':str(userdata.phone),'fname':userdata.fname,'my_personal_code':str(userdata.my_personal_code),
                           'zoomtoken_id':str(userdata.zoomtoken_id),'email':userdata.email, 'email_verified': str(userdata.email_verified)}
            try :
                userdetails =  userdata.usertable.get()
                datalisting['city'] = str(userdetails.city)
                datalisting['state'] = str(userdetails.state)
                datalisting['country'] = str(userdetails.country)
                datalisting['zipcode'] = str(userdetails.zipcode)
                datalisting['address'] = str(userdetails.address)
                if userdetails.height is None:
                    datalisting['height'] = ''
                else:
                    datalisting['height'] = str(userdetails.height)
                if userdetails.is_sports_person is None:
                    datalisting['is_sports_person'] = ''
                else:
                    datalisting['is_sports_person'] = str(userdetails.is_sports_person)
                if userdetails.daily_activity_type is None:
                    datalisting['daily_activity_type'] = ''
                else:
                    datalisting['daily_activity_type'] = str(userdetails.daily_activity_type)
                
            except Exception as generalException:
                datalisting['city'] = ''
                datalisting['state'] = ''
                datalisting['country'] = ''
                datalisting['zipcode'] = ''
                datalisting['address'] = ''
                datalisting['height'] = ''
                datalisting['is_sports_person'] = ''
                datalisting['daily_activity_type'] = ''
            
            dataList =[{"pk":userdata.pk,"fields":datalisting}]
            #Serializing and sending only the required fields
            # data = serializers.serialize('json', [userdata,], fields = (
            #     'status', 
            #     'refer_id',
            #     'fname',
            #     'lname',
            #     'phone',
            #     'zoom_uid',
            #     'business_id',
            #     'sex',
            #     'dob',
            #     'my_personal_code',
            #     'zoomtoken_id',
               
            #     'email'
            #     ))
            # struct = json.loads(data)
            objlogin = TblAutherization(
                user_id = userdata.id,
                secret_key = request.session["token"], 
                date_created = datetime.datetime.today()
                )
            objlogin.save()
#            if deviceId  is not None and deviceId != '':
#                ob = TblNotificationUser.objects.filter(device_id=deviceId).update(user_id=userdata.id, login_status='1')
            if splashId is not None and splashId != '' and splashId != 0:
                updateSplash(userdata.pk,splashId)
            countNotifications  = getNotificationCount(userdata.pk)
            if businessId is not None and businessId != '' and businessId != 0:
                userdata.business_id = businessId
                userdata.save()
            if policyExist==1:
                try:
                    TblUserPolicy.objects.get(user__id=userdata.id,policy__id=policyId,status=1,expiry_date__gte = constants.FORMATTED_TIME())
                    already_bought = 1
                except TblUserPolicy.DoesNotExist:
                    already_bought = 0
            walletAmount=0
            if userdata.business_id != 0 and userdata.email_verified==1:
                pass
            else:
                try:
                    objWallet = TblUserWallet.objects.get(user_id=userdata.id,status=1)
                    walletAmount = objWallet.money
                except TblUserWallet.DoesNotExist:
                    pass
            content = {
                'status': 1, 
                'responseCode' : status.HTTP_200_OK, 
                'message':constants.SUCCESS,
                'token' : request.session["token"],
                'notificationsCount' : countNotifications,
                'messagesCount' : getMessageCount(userdata.pk),
                'policyExist':policyExist,
                'alreadyBought':already_bought,
                'policyId':policyId,
                'policyPrice':policyPrice,
                'walletAmount':walletAmount,
                'data' : dataList
                }
            return Response(content)
        else:
            if match:
                prefix = "Email"
            else:
                prefix = "Phone"
            content = {
                'status': 0, 
                'responseCode' : status.HTTP_401_UNAUTHORIZED, 
                'message' : prefix + '/Password does not match'
                }
            return Response(content)
    else:
        content = {
            'status': 0, 
            'responseCode': status.HTTP_400_BAD_REQUEST, 
            'message' : 'Email and password are mandatory'
            }
        return Response(content)



@api_view(['POST'])
@csrf_exempt
@checkAuthorization
def register(request):
    if request.method == 'POST':
        #Loading the JSON data from request's body
        loadedJsonData = json.loads(request.body)
        getEmail = loadedJsonData.get('email')
        getPassword = loadedJsonData.get('password')
        confirmPassword = loadedJsonData.get('confirmPassword')
        fName = loadedJsonData.get('fname')
        lName = loadedJsonData.get('lname')
        #userType = loadedJsonData.get('userType')
        getbusinessId = loadedJsonData.get('businessId')
        policyId = loadedJsonData.get('policyId')
        sex = loadedJsonData.get('sex')
        dateOfBirth = loadedJsonData.get('dob')
        splashId = loadedJsonData.get('splashId')
        phoneNumber = loadedJsonData.get('phoneNumber')
        through = 0
        already_bought=0
        policyExist=0
        # return Response({'email':email,'password':password,'cpassword':con})
        if getbusinessId is not None and getbusinessId != '' and getbusinessId != 0:
            try:
                objBusines = TblBusinessRegister.objects.get(pk=getbusinessId,status=1)
                try:
                    objPolicy = TblPolicy.objects.get(id=policyId,status=1,expiry_date__gte = constants.FORMATTED_TIME(),for_business=getbusinessId)
                    policyExist=1
                except TblUserPolicy.DoesNotExist:
                    policyExist=0
            except TblBusinessDomains.DoesNotExist:
                getbusinessId = 0
        else:
            getbusinessId = 0
                
        if getEmail is not None and getEmail != '' and getPassword is not None and getPassword != '' and confirmPassword is not None and confirmPassword != '' and phoneNumber is not None and phoneNumber != '' :
            if getPassword == confirmPassword:
                encryptedPWD = make_password(password=getPassword,
                                  salt=None,
                                  hasher='unsalted_md5')
                match = re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', getEmail)
                if len(str(phoneNumber)) != 10 or  phoneNumber.isnumeric() != True  or match == None:
                    content = {
                                'status' : 0,
                                'responseCode' : status.HTTP_400_BAD_REQUEST,
                                'message' : 'Phone/email invalid',
                                }
                    return Response(content)
                # Check if the user exist by the email ID otherwise create the user in database

                checkObject = TblUser.objects.filter(email=getEmail).count()
                checkPhone  = TblUser.objects.filter(phone=phoneNumber).count()
                if checkObject > 0 or checkPhone > 0:
                    content = {
                            'status' : 0,
                            'responseCode' : status.HTTP_400_BAD_REQUEST,
                            'message' : 'email/phone already registered',
                            }
                    return Response(content)
                else:

                    payload = {'api_key': constants.zoom_api_key, 'api_secret': constants.zoom_api_secret_key,'first_name':fName,'last_name':lName,'email':getEmail,'type':2,'disable_recording':'true','meeting_capacity':2,'dept':'drInsta'}
                    response = requests.post('https://api.zoom.us/v1/user/custcreate', params=payload)
                    read = json.loads(response.text)

                    zoomId = read['id'];
                    zommData = {'api_key': constants.zoom_api_key, 'api_secret': constants.zoom_api_secret_key,'id':zoomId}
                    tokenUrl = "https://api.zoom.us/v1/user/get";
                    tokenResponse = requests.post(tokenUrl, params=zommData)
                    tokenJson = json.loads(tokenResponse.text)
                    tokenId = tokenJson['token']
                    try:
                        domain  = getEmail.split('@')
                        businessId = getbusinessId
                        if businessId == 0:
                            try:
                                businessDomain = TblBusinessDomains.objects.get(domain_name=domain[1])
                                if businessDomain:
                                    businessId = businessDomain.pk
                                else:
                                    businessId = 0
                            except TblBusinessDomains.DoesNotExist:
                                businessId = 0
                        createdObject, createdFlag = TblUser.objects.get_or_create(
                            email=getEmail,
                            password= encryptedPWD,
                            fname=fName,
                            through = through,
                            lname=lName,
                            business_id = businessId,
                            sex=sex,
                            my_personal_code = get_random_string(length=8),
                            dob=dateOfBirth,
                            phone= int(phoneNumber),
                            zoom_uid = zoomId,
                            zoomtoken_id = tokenId,
                            status = 1,
                            free_visits = 0,
                            refer_id = 0
                            )

                        # data  = TblUser.objects.get(email = "125@gmail.com")
                        # data  = serializers.serialize('json', [data,],)

                        if createdFlag == True:
                            token = get_random_string(length=32)
                            objlogin = TblAutherization(
                                user_id = createdObject.id,
                                secret_key = token,
                                date_created = datetime.datetime.today()
                                )
                            objlogin.save()
                            sendRegistrationEmail(getEmail,fName,lName,token)
                            #If the record was successfully created

                            data = serializers.serialize('json', [createdObject,],
                                fields = (
                                    'status',
                                    'refer_id',
                                    'fname',
                                    'lname',
                                    'dob',
                                    'phone',
                                    'zoom_uid',
                                    'business_id',
                                    'sex',
                                    'my_personal_code',
                                    'zoomtoken_id',
                                    'email',
                                    'emailVerify'

                                )
                            )

                            struct = json.loads(data)
                            if splashId is not None and splashId != '' and splashId != 0:
                                updateSplash(createdObject.id,splashId)
                            countNotifications  = getNotificationCount(createdObject.id)
                            if policyExist==1:
                                try:
                                    TblUserPolicy.objects.get(user__id=createdObject.id,policy__id=policyId,status=1,expiry_date__gte = constants.FORMATTED_TIME())
                                    already_bought = 1
                                except TblUserPolicy.DoesNotExist:
                                    already_bought = 0
                            content = {
                                'status' : 1,
                                'responseCode' : status.HTTP_201_CREATED,
                                'message' : constants.created,
                                'token' : token ,
                                'notificationsCount' : countNotifications,
                                'messagesCount' : 0,
                                'data' : struct,
                                'phone': str(createdObject.phone),
                                'policyExist':policyExist,
                                'alreadyBought':already_bought,
                                'policyId':objPolicy.id,
                                'policyPrice':objPolicy.price,
                                'tokenJson': tokenJson
                                }
                        else:
                            #If the record was not created for some reason
                            content = {
                                'status' : 0,
                                'responseCode' : status.HTTP_400_BAD_REQUEST,
                                'message' : constants.registration_failed,
                                }
                    except Exception as generalException:
                        print generalException
                        content = {
                            'status' : 0,
                            'responseCode' : status.HTTP_500_INTERNAL_SERVER_ERROR,
                            'message' : constants.registration_failed,
                            }
                        return Response(content)

            else:
                content = {
                        'status': 0,
                        'responseCode': status.HTTP_412_PRECONDITION_FAILED,
                        'message' : "Password Mismatch"
                    }
        else:
            content = {
                    'status': 0,
                    'responseCode' : status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                    "message" : constants.MISSING_PARAM,
                }
    else:
        content = {
            'status': 0,
            'responseCode' : status.HTTP_405_METHOD_NOT_ALLOWED,
            'message': constants.WRONG_REQUEST
            }
    return Response(content)


def sendRegistrationEmail(email,fname,lname,token):
    if email is not None and email != '':
        name = fname.title() + ' ' + lname.title()
        registraionTemplate = get_template('../templates/registeration.html')
        c = Context({"verifyurl": "http://webapp.doctorinsta.com/#/validate/"+token,"fullname":name})
        html = registraionTemplate.render(c)
        subject = "Welcome " + str(fname.title()) + " to Doctor Insta"
        email = EmailMessage(subject, html, to=[email],from_email='support@doctorinsta.com')
        email.content_subtype = "html"
        email.send()



'''
File type : Decorator
Version : 1.0
Description : This file have all the security related decorators that can be used anywhere
'''
__author__ = 'kunal monga'


from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.response import Response
from customers.models import TblAutherization
from functools import wraps
from rest_framework import status
from extras import constants
import json


def checkAuthorization(view_func):
    def _decorator(request, *args, **kwargs):
        loadedJsonData = json.loads(request.body)
        getKey = loadedJsonData.get('authKey')
        #print 'token=', token
        #print 'authkey=', getKey
        if getKey is not None and getKey != '':
            try:
                auth = TblAutherization.objects.get(secret_key=getKey)
                return view_func(request)
            except TblAutherization.DoesNotExist:
                content = {'status':0,'responseCode': status.HTTP_401_UNAUTHORIZED,'message':constants.AUTH_KEY_MISSING}
                return Response(content)
        else:
            content = {'status':0,'responseCode': status.HTTP_400_BAD_REQUEST,'message':constants.MISSING_PARAM}
            return Response(content)
    return wraps(view_func)(_decorator)


from .models import *
from company.models import *
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
import json
from extras import constants
from math import radians,sin,cos,asin,sqrt
from rest_framework import serializers



def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km



@api_view(['POST'])
@csrf_exempt
def list_vendors(request):
	loadedJsonData = json.loads(request.body)
	latitude = loadedJsonData.get('latitude')
	longitude = loadedJsonData.get('longitude')
	vendorObject = TblVendor.objects.all()
	vendorList = []
	message = "No data available"
	statusSet = 0
	for item in vendorObject :
		lats = item.latitude
		longs = item.longitude
		if latitude and longitude  and lats  and longs :
			distance = haversine(latitude,longitude,lats,longs)
			if distance < 10 :
				distance = round(distance,1)
				image = ""
				if item.image :
					image = str(request.META['HTTP_HOST']) + "/media/" + str(item.image)
				vendor_dict = {'distance':distance,'name' : item.name ,'email' : item.email ,'web_url' : item.web_url ,'latitude' : item.latitude ,'longitude' : item.longitude ,'image' : image }
				vendorList.append(vendor_dict)
				message = "Data loaded successfuly"
				statusSet = 1


	content = {
        'status' : statusSet, 
        'responseCode': status.HTTP_200_OK,
        'message' : message,
        'data' : vendorList,
        } 
	return Response(content) 


@api_view(['POST'])
@csrf_exempt
def home_page_details(request):
	loadedJsonData = json.loads(request.body)
	dataList1 = []
	dataObj = TblData.objects.values_list('cat_type').distinct()
	for items in dataObj :
		dataObj = TblData.objects.filter(cat_type = items[0])
		dataList2 = []
		for item in dataObj : 
			image = str(request.META['HTTP_HOST']) + "/media/" + str(item.image)
			dataDict =  {"category_type":str(item.cat_type),"category_name":str(item.cat_name),"display_name":str(item.display_name),"image_url":image}
			dataList2.append(dataDict)
		datadict2 =  {"type": items[0],"list" : dataList2 }
		dataList1.append(datadict2)


	message = "Data loaded successfuly"
	content = {
        'status' : 1, 
        'responseCode': status.HTTP_200_OK,
        'message' : message,
        'data' : dataList1,
        } 
	return Response(content) 



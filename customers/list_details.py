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
			if distance < 100 :
				distance = round(distance,1)
				image = ""
				if item.cover_photo :
					image = str(request.META['HTTP_HOST']) + "/media/" + str(item.cover_photo)
				vendor_dict = {'vendor_id':item.id,'distance':distance,'name' : item.name ,'email' : item.email ,'web_url' : item.web_url ,'latitude' : item.latitude ,'longitude' : item.longitude ,'image' : image }
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
			image = ""
			if item.image :
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


@api_view(['POST'])
@csrf_exempt
def list_category_vendors(request):
	loadedJsonData = json.loads(request.body)
	latitude = loadedJsonData.get('latitude')
	longitude = loadedJsonData.get('longitude')
	category = loadedJsonData.get('category')
	vendorObject = TblVendor.objects.all()
	vendorList = []
	message = "No data available"
	statusSet = 0
	for item in vendorObject :
		lats = item.latitude
		longs = item.longitude
		if latitude and longitude  and lats  and longs :
			distance = haversine(latitude,longitude,lats,longs)
			if distance < 100  and category in item.category:
				distance = round(distance,1)
				image = ""
				if item.cover_photo :
					image = str(request.META['HTTP_HOST']) + "/media/" + str(item.cover_photo)
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
def vendor_details(request):
	loadedJsonData = json.loads(request.body)
	vendor_id = loadedJsonData.get('vendor_id')
	latitude = loadedJsonData.get('latitude')
	longitude = loadedJsonData.get('longitude')
	vendorObject = TblVendor.objects.filter(id = vendor_id)
	print vendorObject,'ewefsf'
	vendorList = []
	message = "No data available"
	statusSet = 0
	if vendorObject.count() > 0 :
		item = vendorObject[0]
		lats = item.latitude
		longs = item.longitude
		distance = ""
		if latitude and longitude  and lats  and longs :
			distance = haversine(latitude,longitude,lats,longs)
			distance = round(distance,1)
		cover_photo = ""
		food_menu = ""
		drinks_menu = ""
		dessert_menu = ""
		cafe_menu = ""

		if item.cover_photo :
			cover_photo = str(request.META['HTTP_HOST']) + "/media/" + str(item.cover_photo)
		if item.food_menu :
			food_menu = str(request.META['HTTP_HOST']) + "/media/" + str(item.food_menu)
		if item.drinks_menu :
			drinks_menu = str(request.META['HTTP_HOST']) + "/media/" + str(item.drinks_menu)	
		if item.dessert_menu :
			dessert_menu = str(request.META['HTTP_HOST']) + "/media/" + str(item.dessert_menu)	
		if item.cafe_menu :
			cafe_menu = str(request.META['HTTP_HOST']) + "/media/" + str(item.cafe_menu)	

		vendor_dict = {
				"vendor_id":item.id,
				'distance':distance,
				'name' : item.name ,
				'email' : item.email ,
				'web_url' : item.web_url ,
				'latitude' : item.latitude ,
				'longitude' : item.longitude ,
				'image' : cover_photo,
				"mon_op_timings" : item.mon_op_timings,
				"mon_close_timings" : item.mon_close_timings,
				"tues_op_timings" : item.tues_op_timings,
				"tues_close_timings" : item.tues_close_timings,
				"wed_op_timings" : item.wed_op_timings,
				"wed_close_timings" : item.wed_close_timings,
				"thurs_op_timings" : item.thurs_op_timings,
				"thurs_close_timings" : item.thurs_close_timings,
				"fri_op_timings" : item.fri_op_timings,
				"fri_close_timings" : item.fri_close_timings,
				"sat_op_timings" : item.sat_op_timings,
				"sat_close_timings" : item.sat_close_timings,
				"sun_op_timings" : item.sun_op_timings,
				"sun_close_timings" : item.sun_close_timings,
				"food_menu" : food_menu,
				"drinks_menu" : drinks_menu,
				"dessert_menu" : dessert_menu,
				"cafe_menu" : cafe_menu,
				"category" : item.category,
				"cuisines" : item.cuisines,
				"ambience" : item.ambience,
				"special_offerings" : item.special_offerings,
				"ordering_options" : item.ordering_options,
				"cost_for_two" : item.cost_for_two,
				"payment_modes" : item.payment_modes,
				"facilities" : item.facilities,
				"contact_person" : item.contact_person,
				"phone_contact_person" : item.phone_contact_person,
				"address" : item.address,
				"phone" : item.phone
			 }

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


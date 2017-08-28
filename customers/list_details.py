from .models import *
from company.models import *
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
import json
import ast
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
	print dataObj,'sqdqed'
	for items in dataObj :
		dataObj = TblData.objects.filter(cat_type = items[0])
		dataList2 = []
		for item in dataObj : 
			image = ""
			if item.image :
				image = str(request.META['HTTP_HOST']) + "/media/" + str(item.image)
			dataDict =  {"category_id":item.id,"category_type":str(item.cat_type),"category_name":str(item.cat_name),"display_name":str(item.display_name),"image_url":image}
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
	message = "No data available"
	statusSet = 0
	loadedJsonData = json.loads(request.body)
	latitude = loadedJsonData.get('latitude')
	longitude = loadedJsonData.get('longitude')
	category_id = loadedJsonData.get('category_id')
	catagory_data = TblData.objects.filter(id=category_id)
	if len(catagory_data) > 0:
		category_type = catagory_data[0].cat_type
		display_name = catagory_data[0].display_name
		if category_type == "category" :
			input_dict = constants.category_dict
		elif  category_type == "ambience" :
			input_dict = constants.ambience_dict
		elif  category_type == "special_offerings" :
			input_dict = constants.special_offerings_dict
		for key, value in input_dict.iteritems():
			if value.lower() == display_name.lower() :
				category_key = key
	else :
		content = {
	        'status' : statusSet,
	        'responseCode': status.HTTP_200_OK,
	        'message' : message,
	        'data' : [],
	        }
		return Response(content)

	vendorObject = TblVendor.objects.all()
	vendorList = []
	
	for item in vendorObject :
		lats = item.latitude
		longs = item.longitude
		if latitude and longitude  and lats  and longs :
			distance = haversine(latitude,longitude,lats,longs)
			if distance < 100  and category_key in eval("item."+category_type):
				distance = round(distance,1)
				image = ""
				if item.cover_photo :
					image = str(request.META['HTTP_HOST']) + "/media/" + str(item.cover_photo)
				vendor_dict = {"vendor_id":item.id,'distance':distance,'name' : item.name ,'email' : item.email ,'web_url' : item.web_url ,'latitude' : item.latitude ,'longitude' : item.longitude ,'image' : image }
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

		category_list = []
		cuisines_list = []
		ambience_list = []
		special_offerings_list = []
		cost_for_two_list = []
		payment_modes_list = []
		facilities_list = []

		category = ast.literal_eval(item.category)
		cuisines = ast.literal_eval(item.cuisines)
		ambience = ast.literal_eval(item.ambience)
		special_offerings = ast.literal_eval(item.special_offerings)
		payment_modes = ast.literal_eval(item.payment_modes)
		facilities = ast.literal_eval(item.facilities)

		for i in category :
			i = str(i)
			category_list.append( {"id":i,"type": constants.category_dict[i]})
		for i in cuisines :
			i = str(i)
			cuisines_list.append( {"id":i,"type": constants.cuisines_dict[i]})
		for i in ambience :
			i = str(i)
			ambience_list.append( {"id":i,"type": constants.ambience_dict[i]})
		for i in special_offerings :
			i = str(i)
			special_offerings_list.append( {"id":i,"type": constants.special_offerings_dict[i]})

		cost_for_two_list.append( {"id":i,"type": constants.cost_for_two_dict[item.cost_for_two]})
		for i in payment_modes :
			i = str(i)
			payment_modes_list.append( {"id":i,"type": constants.payment_modes_dict[i]})
		for i in facilities :
			i = str(i)
			facilities_list.append( {"id":i,"type": constants.facilities_dict[i]})

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

		menu_list = [{	
					"food_menu" : food_menu,
					"drinks_menu" : drinks_menu,
					"dessert_menu" : dessert_menu,
					"cafe_menu" : cafe_menu
					}]

		timing_list = [ 
						{
						"day" :"Monday",
						"opening_timing" : item.mon_op_timings,
						"closing_timing" : item.mon_close_timings,
						},
						{
						"day" :"Tuesday",
						"opening_timing" : item.tues_op_timings,
						"closing_timing" : item.tues_close_timings,
						},
						{
						"day" :"Wednesday",
						"opening_timing" : item.wed_op_timings,
						"closing_timing" : item.wed_close_timings,
						},
						{
						"day" :"Thursday",
						"opening_timing" : item.thurs_op_timings,
						"closing_timing" : item.thurs_close_timings,
						},
						{
						"day" :"Friday",
						"opening_timing" : item.fri_op_timings,
						"closing_timing" : item.fri_close_timings,
						},
						{
						"day" :"Saturday",
						"opening_timing" : item.sat_op_timings,
						"closing_timing" : item.sat_close_timings,
						},
						{
						"day" :"Sunday",
						"opening_timing" : item.sun_op_timings,
						"closing_timing" : item.sun_close_timings,
						}
					]


		vendor_dict = {
				"vendor_id":item.id,
				'distance':distance,
				'name' : item.name ,
				'email' : item.email ,
				'web_url' : item.web_url ,
				'latitude' : item.latitude ,
				'longitude' : item.longitude ,
				'image' : cover_photo,
				"menu_list" : menu_list,
				"timing_list" : timing_list,
				"category" : category_list,
				"cuisines" : cuisines_list,
				"ambience" : ambience_list,
				"special_offerings" : special_offerings_list,
				"ordering_options" : item.ordering_options,
				"cost_for_two" : cost_for_two_list,
				"payment_modes" : payment_modes_list,
				"facilities" : facilities_list,
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


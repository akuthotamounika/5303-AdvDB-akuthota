from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_restful import reqparse
from flask import jsonify
from flask_cors import CORS, cross_origin

#from pymongo import MongoClient
import pymongo
from bson import Binary, Code
from bson.json_util import dumps
from bson.objectid import ObjectId

import datetime

import json
import urllib


import timeit

app = FlaskAPI(__name__)
CORS(app)

client = pymongo.MongoClient('localhost', 27017)
db = client['akuthota']
businessdb = db['yelp.business']
review = db['yelp.review']
userdb = db['yelp.user']
tipdb = db['yelp.tip']

parser = reqparse.RequestParser()

"""=================================================================================="""
"""=================================================================================="""
"""=================================================================================="""


@cross_origin() # allow all origins all methods.
@app.route("/", methods=['GET'])
def index():
 """Print available functions."""
 func_list = {}
 for rule in app.url_map.iter_rules():
 if rule.endpoint != 'static':
 func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
 return func_list

 
"""=================================================================================="""
"""Find all restaurants with zip code X or Y"""
@app.route("/zip/<args>", methods=['GET'])
def findzips(args):

 args = myParseArgs(args)
 
 start= int(args['start'])
 
 end = int(args['limit'])
 
 data = []
 zip = []
 
 zip = args['zip'].split(',') 
 
 result = businessdb.find({},{'_id':0}) 
 
 
 for r in result:
 parts = r['full_address'].split(' ')
 target = parts[-1]
 if target in zip and start < end : 
 data.append(r['business_id'])
 start += 1
	
 return {"count":data} 

"""=================================================================================="""
@app.route("/user/<args>", methods=['GET'])
def user(args):

 args = myParseArgs(args)
 
 if 'skip' in args.keys():
 args['skip'] = int(args['skip'])
 if 'limit' in args.keys():
 args['limit'] = int(args['limit'])

 data = []
 
 #.skip(1).limit(1)
 
 if 'skip' in args.keys() and 'limit' in args.keys():
 result = userdb.find({},{'_id':0}).skip(args['skip']).limit(args['limit'])
 elif 'skip' in args.keys():
 result = userdb.find({},{'_id':0}).skip(args['skip'])
 elif 'limit' in args.keys():
 result = userdb.find({},{'_id':0}).limit(args['limit'])
 else:
 result = userdb.find({},{'_id':0}).limit(10) 

 for row in result:
 data.append(row)


 return {"data":data}
 

"""================================================================================="""
@app.route("/business/<args>", methods=['GET'])
def business(args):

 args = myParseArgs(args)
 
 data = []
 
 result = businessdb.find({},{"full_address":1,"_id":0})
 
 for row in result:
 data.append(row)
 

 return {"data":data}
	
"""===================================================================="""
"""Find all restaurants in city X"""

@app.route("/city/<args>", methods=['GET'])
def city(args):
 
 args = myParseArgs(args)
 
 begin = int(args['start'])
 
 terminate = int(args['limit'])

 data = []
 city1 = args['city'] 
 result = businessdb.find({},{'_id':0}) 
 for r in result:
 value = r['city'] 
 if value == city1 and begin < terminate : 
 data.append(r['business_id'])
 begin += 1 
 return {"data":data}
"""==========================================================="""
"""Find the restaurants within 5 miles of lat , lon""" 
@app.route("/closest/<args>", methods=['GET'])
def closestlocation(args):

 args = myParseArgs(args)
 lat = float(args['lat'])
 lon = float(args['lon'])
	
 
 if 'skip' in args.keys():
 args['skip'] = int(args['skip'])
 if 'limit' in args.keys():
 args['limit'] = int(args['limit'])

 data = []
 
 #.skip(1).limit(1)
 
 if 'skip' in args.keys() and 'limit' in args.keys():
 result = businessdb.find({
 "loc": {
 "$geoWithin": { "$center": [[lon,lat] , .004 ] }
 } 
}).skip(args['skip']).limit(args['limit'])
 elif 'skip' in args.keys():
 result = businessdb.find({
 "loc": {
 "$geoWithin": { "$center": [[lon,lat] , .004 ] }
 } 
}).skip(args['skip'])
 elif 'limit' in args.keys():
 result = businessdb.find({
 "loc": {
 "$geoWithin": { "$center": [[lon,lat] , .004 ] }
 } 
}).limit(args['limit'])
 else:
 result = businessdb.find({
 "loc": {
 "$geoWithin": { "$center": [[lon,lat] , .004 ] }
 } 
}).limit(10) 
 
 
 for r in result:
 data.append(r['business_id'])
 return {"data":data} 
"""============================================================""" 
"""Find all the reviews for restaurant X"""
@app.route("/reviews/<args>", methods=['GET'])
def reviews(args):

 args = myParseArgs(args)
 begin = int(args['start'])
 terminate = int(args['limit'])

 data = []
 
 id1 = args['id']
 result = review.find()
 for r in result:
 value = r['business_id']

 if value == id1 and begin < terminate:
 data.append(r['business_id'])
 begin += 1
 return {"count":len(data)} 
"""============================================================="""
"""Find all the users that are considered elite."""
@app.route("/elite/<args>", methods=['GET'])
def find_elite(args):

 args = myParseArgs(args) 
 begin = int(args['start'])
 terminate = int(args['limit'])
 
 data = [] 
 result = userdb.find()
 for r in result:
 target = r['elite']
 if len(target) != 0 and begin < terminate: 
 data.append(r['user_id'])
 begin += 1
 return {"data":data} 
	
	
"""=========================================================="""
"""Find the longest elite user."""
@app.route("/longelite/<args>/", methods=['GET'])
def longelite(args):

 
 
 args = myParseArgs(args) 
 begin = int(args['start'])
 terminate = int(args['limit'])
 
 data = [] 
 
 
 result = userdb.find()
 
 for r in result: 
 
 data1=len(r['elite'])
 if data1 == 12 and begin < terminate:
	
 data.append(r['name'])
 begin += 1
 
	
 return {"data":data} 
""""========================================================="""

 
"""=========================================================="""
"""Find all the reviews for restaurant X that are 5 stars."""	

@app.route("/stars/<args>", methods=['GET'])
def stars(args):

 args = myParseArgs(args)
 begin = int(args['start'])
 terminate = int(args['limit'])
 data = []
 
 args['num_stars'] = int(args['num_stars'])
 novalue = args['num_stars']
 result = review.find()
 for r in result:
 parts = r['stars']
 
 if parts == novalue and begin < terminate:
 data.append(r['business_id'])
 return {"data":len(data)}
	
"""============================================================="""
"""Find all the users that have been 'yelping' for over 5 years."""
@app.route("/yelping/<args>", methods=['GET'])
def yelpingsince(args):

 args = myParseArgs(args)
 
	
 
 if 'skip' in args.keys():
 args['skip'] = int(args['skip'])
 if 'limit' in args.keys():
 args['limit'] = int(args['limit'])

 data = []
 
 #.skip(1).limit(1)
 
 if 'skip' in args.keys() and 'limit' in args.keys():
 result = userdbdb.find({ "yelping_since" : {"$lte":"2011-11"}}, {"_id":0,"name":1}).skip(args['skip']).limit(args['limit'])
 elif 'skip' in args.keys():
 result = businessdb.find({ "yelping_since" : {"$lte":"2011-11"}}, {"_id":0,"name":1}).skip(args['skip'])
 elif 'limit' in args.keys():
 result = businessdb.find({ "yelping_since" : {"$lte":"2011-11"}}, {"_id":0,"name":1}).limit(args['limit'])
 else:
 result = userdb.find({ "yelping_since" : {"$lte":"2011-11"}}, {"_id":0,"name":1}).limit(10) 
 
 
 for r in result:
 data.append(r['name'])
 return {"data":data} 
"""====================================================================================="""
"""Of elite users, whats the average number of years someone is elite."""
@app.route("/avg_elite/", methods=['GET'])
def averageuserelite():

 
 
 data = []
 result = userdb.aggregate(
	[
	{
	"$group" : 
	{
	"_id" : "$name", "average" : {"$avg":{"$size" : "$elite"}}
	}
	}
	]
)
 


 for r in result:
 data.append(r) 
 return {"data":data}
"""=========================================================="""


	

"""==============================================================="""
	
"""Find the average review_count for users."""
@app.route("/review_count/", methods=['GET'])
def averagereview():

 """args = myParseArgs(args)"""
 
 data = []
 result = userdb.aggregate(
	[
	{
	"$group" : 
	{
	"_id" : "$user_id", "averagereviewcount" : {"$avg":"$review_count"}
	}
	}
	]
)
 


 for r in result:
 data.append(r) 
 return {"data":(data)}
	
 
"""=================================================================================="""


"""=================================================================================="""
@app.route("/most_likes/<args>", methods=['GET'])
def find_mostlikes(args):
 args = myParseArgs(args)
 start= int(args['start'])
 end= int(args['limit'])

 data = []
 result = tipdb.find()
 for r in result:
 data.append(r['likes'])
 return {"data":max(data)}
	

"""======================================================================================="""

"""========================================================================================"""

"""========================================================================================"""
def snap_time(time,snap_val):
 time = int(time)
 m = time % snap_val
 if m < (snap_val // 2):
 time -= m
 else:
 time += (snap_val - m)
 
 if (time + 40) % 100 == 0:
 time += 40
 
 return int(time)

"""=================================================================================="""
def myParseArgs(pairs=None):
 """Parses a url for key value pairs. Not very RESTful.
 Splits on ":"'s first, then "=" signs.
 
 Args:
 pairs: string of key value pairs
 
 Example:
 
 curl -X GET http://cs.mwsu.edu:5000/images/
 
 Returns:
 json object with all images
 """
 
 if not pairs:
 return {}
 
 argsList = pairs.split(":")
 argsDict = {}

 for arg in argsList:
 key,val = arg.split("=")
 argsDict[key]=str(val)
 
 return argsDict
 

if __name__ == "__main__":
 app.run(debug=True,host='0.0.0.0',port=5000)

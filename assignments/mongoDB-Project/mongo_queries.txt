Name: Akuthota Mounika
Name: Sheema Rohi
1)Find all restaurants with zip code X or Y -Using 89117 and 89122
db.yelp.business.find({$or: [{"full_address":{$regex: '89117'}},{"full_address":{$regex: '89122'}}]}).count()

db.yelp.business.find({$or: [{"full_address":{$regex: '75205'}},{"full_address":{$regex: '75225'}}]}).pretty()

2)Find all restaurants in city X
db.yelp.business.find({"full_address":{$regex: 'Las Vegas'}}).count()

3)Find the restaurants within 5 miles of lat , lon
db.yelp.business.find({
   loc: {
        $geoWithin: { $center: [ [ -80.839186,35.226504] , .004 ] }
   }
})

4)Find all the reviews for restaurant X
db.yelp.review.find({"business_id":"hB3kH0NgM5LkEWMnMMDnHw"}).count() 

5)Find all the reviews for restaurant X that are 5 stars.
db.yelp.review.find({"business_id":"P1fJb2WQ1mXoiudj8UE44w","stars":5}).count() 

6)Find all the users that have been 'yelping' for over 5 years.
db.yelp.user.aggregate(
   [
     {
       $project:
          {
         year: { $substr: [ "$yelping_since", 2, 2 ] }
          }
      }
   ]
)

7)Find the business that has the tip with the most like
db.yelp.tip.find({},{business_id :1,likes:1}).sort({likes:-1}).limit(1)

8)Find the average review_count for users

db.yelp.user.aggregate(
   [
     {
       $group:
         {
           _id: "$name",
           avgreviewcount: { $avg: "$review_count" }
         }
     }
   ]
)



9)Find all the users that are considered elite.
db.yelp.user.find({"elite":{"$ne":[]}},{"_id":0,"user_id":1,"name":1,"elite":1})

10)Find the longest elite user.
db.yelp.user.aggregate([{$group : {_id : "$user", longest : {$max :{$size : "$elite"}}}}])

11)Of elite users, whats the average number of years someone is elite.
db.yelp.user.aggregate([{$group : {_id : "$name", average : {$avg:{$size : "$elite"}}}}])


Difficult:

5)Find all restaurants with over a 3.5 star rating average rating.
var x =db.yelp.business.aggregate([{$group : {_id : "$name", average : {$avg:"$stars"}}}])
x.forEach(function(d) {print(d.average);})

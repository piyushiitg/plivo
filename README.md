plivo
=====

Suggestion For Movie by Plivo API and XML


How to test:

1. Use Make call api for movie

http://54.251.117.109:9090/plivo/makecall/?number=sip:piyush130322025614@phone.plivo.com&movie=Dhoom

Input:
if movie name is not specified the it will do for Hangover

number is any sip number or phone number that plivo can call 

Response: 
<Response>
<status>201</status>
<call_id>6fd3e550-95fd-11e2-b758-22000abc8f59</call_id>
<message>call fired</message>
</Response>

2. There are 5 questions asked, after that it will tell the avg_rating of the movie. 

3. Ratings url tell the avg rating of all movie

http://54.251.117.109:9090/plivo/ratings/



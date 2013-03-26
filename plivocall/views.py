from django.shortcuts import render_to_response
from django.http import HttpResponse
from plivocall.models import Call,QuestionRatings,CDR
import plivo
import settings
from django.db.models import *
questions = {'0':'How would you rate music composition','1':'How much you rate for story line','2':'How would you rate actors as per their character','3':'How would you rate for dialogs', '4':'How would you rate overall performance for the movie'}
MAX_QUESTIONS = 5
def  plivo_start(request):
    return render_to_response('plivo.html')

def makecall(request):
    import plivo
    called = request.REQUEST.get('number','sip:piyush130322025614@phone.plivo.com')
    movie = str(request.REQUEST.get('movie','Hangover')).lower()
    auth_id = "MAYWY1NTG3M2YWOGU2NT"
    auth_token = "NTAyNmU1NjcyNmIxNTA4YTYxYmMxYTMyNGQ5ZjUw"    
    p = plivo.RestAPI(auth_id, auth_token)
    params = {
    'from': '1212121212', # Caller Id
    'to' : '', # User Number to Call
    #'answer_url' : "https://s3.amazonaws.com/plivosamplexml/speak_url.xml",
    'answer_url' : "http://54.251.117.109:9090/plivo/answer/",
    'hangup_url' : "http://54.251.117.109:9090/plivo/hangup/",
    'answer_method' : "GET",
    'hangup_method' : "GET",
    }
    params['to'] = str(called)
    response = p.make_call(params)
    print '#####################################',params
    status = response[0]
    result = response[1]
    if result.has_key('error'):
        message = result['error']
        api_id = result['api_id']
        request_uuid = ''
    if result.has_key('message'):
        message = result['message']
        request_uuid = result['request_uuid']
        api_id = result['api_id']
    x = '''<Response>
           <status> %s </status>
           <call_id> %s </call_id>
           <message> %s </message>
           </Response>'''%(status,api_id,message)
    if status == 201:
        c = Call.objects.create(status=status,message=message,request_uuid=request_uuid,api_id=api_id,called=called,movie=movie)
    return HttpResponse(x,content_type='application/xml')


def plivo_answer(request):
    x2 = request.REQUEST.get('Digits',0)
    call_uuid = request.REQUEST.get('CallUUID',None)
    try:
        qr = QuestionRatings.objects.filter(call_uuid=call_uuid)
        print call_uuid,'*********************************************'
        qr_len = qr.count()
        if len(qr) != 0:
            qr = QuestionRatings.objects.get(call_uuid=call_uuid,question=qr_len-1)
            qr.rating = x2
            qr.save()
        if qr_len < MAX_QUESTIONS:
            q = questions[str(qr_len)]
       
            x1 = '''<Response>
             <GetDigits action="http://54.251.117.109:9090/plivo/answer/" method="GET">
             <Speak>%s, Press 5 for excellent and 1 for poor, followed by the hash key</Speak>
             </GetDigits>
              <Speak>Input not received. Thank you</Speak>
              </Response>'''%q

            qr = QuestionRatings.objects.create(call_uuid=call_uuid,question=qr_len,rating=x2)
            response = x1
        else:
            avg_rating = calculate_rating(call_uuid)
            x2 = '''<Response>
              <Speak>Your Overall Rating is %s. Thank you</Speak>
              </Response>'''%str(avg_rating)
            response = x2
        return HttpResponse(response,content_type='application/xml')
    except:
        import traceback
        print traceback.format_exc()

def calculate_rating(call_uuid):
    avg_rating = 0
    qr = QuestionRatings.objects.filter(call_uuid=call_uuid)
    for q1 in qr:
        x = q1.rating
        if x > 5:
            x = 5
        avg_rating = avg_rating + q1.rating
    avg_rating = avg_rating/MAX_QUESTIONS
    print "*******************************************************",avg_rating
    return avg_rating

def plivo_hangup(request):
    call_uuid = request.REQUEST.get('CallUUID',None)
    req_uuid = request.REQUEST.get('RequestUUID',None)
    BillDuration = request.REQUEST.get('BillDuration',None)
    From = request.REQUEST.get('From',None)
    HangupCause = request.REQUEST.get('HangupCause',None)
    To = request.REQUEST.get('To',None)
    CallStatus = request.REQUEST.get('CallStatus',None)
    avg_rating = 0
    qr = QuestionRatings.objects.filter(call_uuid=call_uuid)
    for q1 in qr:
        x = q1.rating
        if x > 5:
            x = 5
        avg_rating = avg_rating + q1.rating
    avg_rating = avg_rating/qr.count()
    try:
        response = "sucess"
        c = Call.objects.get(request_uuid=req_uuid)
        cdr = CDR.objects.create(call_uuid=call_uuid,BillDuration=BillDuration,From=From,HangupCause=HangupCause,To=To,CallStatus=CallStatus,avg_rating=avg_rating,movie=c.movie)
        c.delete() 
        return HttpResponse(response,content_type='application/xml')
    except:
        import traceback
        print traceback.format_exc()


def plivo_ratings(request):
    #moviename = request.REQUEST.get('movie','')
    c = CDR.objects.all().values("movie").annotate(rat=Avg("avg_rating"))
    print c
    rating_dict = {}
    for c1 in c:
       rating_dict[c1['movie']] = c1['rat']
    print rating_dict
    return render_to_response('searchresults.html',{'rating_dict': rating_dict})

     

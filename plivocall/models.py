from django.db import models

# Create your models here.
class Call(models.Model):
    request_uuid = models.CharField(max_length=255)
    called = models.CharField(max_length=255)
    status = models.CharField(max_length=10)
    api_id = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    movie = models.CharField(max_length=255)


class QuestionRatings(models.Model):
    call_uuid = models.CharField(max_length=255)
    question = models.CharField(max_length=255)
    rating  = models.FloatField(default=0)

class CDR(models.Model):
    call_uuid = models.CharField(max_length=255)
    BillDuration = models.CharField(max_length=255)
    From = models.CharField(max_length=255)
    HangupCause = models.CharField(max_length=255)
    To = models.CharField(max_length=255)
    CallStatus = models.CharField(max_length=255)
    avg_rating = models.CharField(max_length=255)
    movie = models.CharField(max_length=255)

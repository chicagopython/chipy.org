import settings
import datetime

from django.db import models
from django.contrib.auth.models import User
from interval.fields import IntervalField

from libs.models import CommonModel

MAX_LENGTH = 255

MEETING = (
    ('Loop', 'Loop Meeting - 2nd Thursday'),
    ('North', 'North Meeting - 3rd Thursday')
)

class Venue(CommonModel):

    def __unicode__(self):
	return self.name

    name = models.CharField(max_length=MAX_LENGTH)
    email = models.EmailField(max_length=MAX_LENGTH,blank=True,null=True)
    phone = models.CharField(max_length=MAX_LENGTH,blank=True,null=True)
    address = models.TextField(blank=True,null=True)

    def get_latitude(self):
        raise NotImplimented

    def get_longitude(self):
        raise NotImplimented

    longitude = property(get_longitude)
    latitude = property(get_latitude)

        
    @property
    def jsonLatLng(self):
        '''
        Use the string returned as args for google.maps.LatLng constructor.
	'''
        if self.latitude != None and self.longitude != None:
            return "%.6f,%.6f" % (self.latitude,self.longitude)
        else:
            return None
    
    directions = models.TextField(blank=True,null=True)
    embed_map = models.TextField(blank=True,null=True)
    link = models.URLField(verify_exists=True, blank=True, null=True)



class Meeting(CommonModel):


    def __unicode__(self):
	if self.where:
	    return "%s at %s" % (self.when.strftime("%A, %B %d %Y at %I:%M %p"), self.where.name)
	return "%s location TBD" % self.when

    when = models.DateTimeField()
    where = models.ForeignKey(Venue,blank=True,null=True)

    def is_future(self):
        return bool( self.when >=  ( datetime.datetime.now() - datetime.timedelta(hours = 3 )))

    def rsvp_user_yes(self):
        raise NotImplimentedError

    def rsvp_user_maybe(self):
        raise NotImplimentedError


class Presentor(CommonModel):
    def __unicode__(self):
        return self.name

    user = models.ForeignKey(User, blank = True, null = True)
    name = models.CharField(max_length = MAX_LENGTH)
    email = models.EmailField(max_length = MAX_LENGTH, blank = True, null = True)
    phone = models.CharField(max_length = MAX_LENGTH, blank = True, null = True)
    release = models.BooleanField(default = False)
    

class Topic(CommonModel):

    def __unicode__(self):
        out = self.title
        if self.presentor:
            out += "By: %s" % self.presentor.name
        return out

    title = models.CharField(max_length=MAX_LENGTH)
    presentor = models.ForeignKey(Presentor,blank=True,null=True)
    meeting = models.ForeignKey( Meeting, blank=True, null=True)
    length = IntervalField(format="M", blank = True, null = True)
    embed_video = models.TextField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    slides_link = models.URLField(verify_exists=True, blank=True, null=True)
    start_time = models.DateTimeField(blank = True, null = True)
    approved = models.BooleanField(default = False)

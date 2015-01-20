from django.core.exceptions import ObjectDoesNotExist
import requests
from apps.meetings.models import Meeting, RSVP


def meetup_meeting_sync(api_key, meetup_event_id):
    url = "http://api.meetup.com/2/rsvps"
    params = dict(key=api_key, event_id=meetup_event_id)
    api_response = requests.get(url, params=params)

    chipy_meeting_instance = Meeting.objects.get(meetup_id=meetup_event_id)

    response = api_response.json()
    results = response['results']

    for result in results:
        meetup_user_id = result['member']['member_id']

        try:
            rsvp = RSVP.objects.get(meetup_user_id=meetup_user_id, meeting=chipy_meeting_instance)
        except ObjectDoesNotExist:
            rsvp = RSVP(meetup_user_id=meetup_user_id, meeting=chipy_meeting_instance)

        rsvp.response = 'Y' if result['response'] == 'yes' else 'N'
        rsvp.name = result['member']['name']
        rsvp.save()
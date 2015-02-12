import logging

from django.core.exceptions import ObjectDoesNotExist
import requests
from apps.meetings.models import Meeting, RSVP


logger = logging.getLogger(__name__)


def get_rsvp(meeting, meetup_member):
    """
    Handles getting the rsvp instance to update from Meetup.
    Will return a new instance if needed.

    If there is a name collision, it will update the current RSVP with the Meetup Info. This isn't perfect by any
    stretch, but for our uses it should be good enough.

    """

    meetup_user_id = meetup_member['member_id']

    name_collisions = RSVP.objects.filter(name=meetup_member['name'], meeting=meeting)

    if name_collisions:
        rsvp = name_collisions[0]
        rsvp.meetup_user_id=meetup_user_id

    else:
        try:
            rsvp = RSVP.objects.get(meetup_user_id=meetup_user_id, meeting=meeting)
        except ObjectDoesNotExist:
            rsvp = RSVP(meetup_user_id=meetup_user_id, meeting=meeting)

    return rsvp


def meetup_meeting_sync(api_key, meetup_event_id):
    url = "http://api.meetup.com/2/rsvps"
    params = dict(key=api_key, event_id=meetup_event_id, page=1000)
    api_response = requests.get(url, params=params)

    meeting = Meeting.objects.get(meetup_id=meetup_event_id)

    response = api_response.json()
    results = response['results']
    logger.info('Got {} results for Meetup sync'.format(len(results)))
    for result in results:
        rsvp = get_rsvp(meeting, result['member'])

        rsvp.response = 'Y' if result['response'] == 'yes' else 'N'
        rsvp.name = result['member']['name']
        rsvp.save()

        logger.info('Saved RSVP for {} with response of {}'.format(result['member']['name'], rsvp.response))
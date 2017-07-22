from __future__ import unicode_literals

import logging

from django.core.exceptions import ObjectDoesNotExist, ValidationError
import requests
from .models import Meeting, RSVP


logger = logging.getLogger(__name__)


def get_rsvp(meeting, meetup_member):
    """
    Handles getting the rsvp instance to update from Meetup.
    Will return a new instance if needed.

    If there is a name collision, it will update the current RSVP with the
    Meetup Info. This isn't perfect by any
    stretch, but for our uses it should be good enough.

    """

    meetup_user_id = meetup_member['member_id']

    name_collisions = RSVP.objects.filter(
        name=meetup_member['name'], meeting=meeting)

    if name_collisions:
        rsvp = name_collisions[0]
        rsvp.meetup_user_id = meetup_user_id

    else:
        try:
            rsvp = RSVP.objects.get(
                meetup_user_id=meetup_user_id, meeting=meeting)
        except ObjectDoesNotExist:
            rsvp = RSVP(meetup_user_id=meetup_user_id, meeting=meeting)

    return rsvp


def get_best_name_available(result, real_names):
    name = " ".join(s.capitalize() for s in result['member']['name'].split())
    real_name = real_names.get(result['member']['member_id'], None)
    name_response = None
    # If "please provide your name" was in the event's question list
    if 'answers' in result:
        for answer in result['answers']:
            if 'question' in answer and 'name' in answer['question'].lower():
                if 'answer' in answer:
                    name_response = answer['answer']
                break
    if name_response:
        return " ".join(s.capitalize() for s in name_response.split())
    elif real_name:
        return real_name
    else:
        return name


def get_real_names(api_key, results):
    real_names = {}
    url = "https://api.meetup.com/2/profiles"
    realname_question_id = 8181568
    attendee_ids = ','.join(str(r['member']['member_id']) for r in results)
    params = dict(member_id=attendee_ids,
                  group_urlname='_ChiPy_',
                  key=api_key)
    api_response = requests.get(url, params=params)
    response = api_response.json()
    results = response['results']
    for result in results:
        id = result['member_id']
        for a in result['answers']:
            if a['question_id'] == realname_question_id:
                if 'answer' in a:
                    real_names[id] = a['answer']
        if id not in real_names:
            real_names[id] = " ".join(s.capitalize() for s in result['name'].split())
    return real_names


def meetup_meeting_sync(api_key, meetup_event_id):
    url = "http://api.meetup.com/2/rsvps"
    params = dict(key=api_key,
                  event_id=meetup_event_id,
                  fields='answer_info',
                  page=1000)
    api_response = requests.get(url, params=params)

    meeting = Meeting.objects.get(meetup_id=meetup_event_id)

    response = api_response.json()
    results = response['results']
    logger.info('Got {} results for Meetup sync'.format(len(results)))
    real_names = get_real_names(api_key, results)

    for result in results:
        rsvp = get_rsvp(meeting, result['member'])

        rsvp.response = 'Y' if result['response'] == 'yes' else 'N'
        rsvp.name = get_best_name_available(result, real_names)
        rsvp.guests = int(result['guests'])
        try:
            rsvp.save()
        except ValidationError as exc:
            logger.warning('Error saving RSVP for {} with response of {}. Error is {}'.format(
                result['member']['name'], rsvp.response, exc))
        else:
            logger.info('Saved RSVP for {} with response of {}'.format(
                result['member']['name'], rsvp.response))

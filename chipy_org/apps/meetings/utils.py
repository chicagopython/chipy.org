from django.core.exceptions import ObjectDoesNotExist
import requests
from apps.meetings.models import Meeting, RSVP


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
    params = dict(member_id=attendee_ids, group_urlname = '_ChiPy_', key=api_key)
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
    params = dict(key=api_key, event_id=meetup_event_id, fields='answer_info')
    api_response = requests.get(url, params=params)

    chipy_meeting_instance = Meeting.objects.get(meetup_id=meetup_event_id)

    response = api_response.json()
    results = response['results']
    real_names = get_real_names(api_key, results)

    for result in results:
        meetup_user_id = result['member']['member_id']

        try:
            rsvp = RSVP.objects.get(meetup_user_id=meetup_user_id, meeting=chipy_meeting_instance)
        except ObjectDoesNotExist:
            rsvp = RSVP(meetup_user_id=meetup_user_id, meeting=chipy_meeting_instance)

        rsvp.response = 'Y' if result['response'] == 'yes' else 'N'
        rsvp.name = get_best_name_available(result, real_names)
        rsvp.guests = int(result['guests'])
        rsvp.save()

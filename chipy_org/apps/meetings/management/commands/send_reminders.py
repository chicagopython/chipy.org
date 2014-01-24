from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from django.utils import timezone

from datetime import date, timedelta
from mailer import send_mail

from apps.meetings.models import Meeting


message = """
Hi {name},

There's a ChiPy meeting {when}. 

Location:
{loc_name}
{phone} / {email}
{address}

Topics:
"""
topic_message = """
{title} by {speaker}
{description}


""" 

class Command(NoArgsCommand):
    help = 'Sends out reminders the Sunday before the meeting and the day of meeting.'

    def handle_noargs(self, **options):
        print("Sending reminders...")
        sunday_of_this_week = timezone.now().date() - timedelta(days=(timezone.now().isocalendar()[2]))
        sunday_of_next_week = sunday_of_this_week + timedelta(days=7)

        for meeting in Meeting.objects.filter(when__gte=sunday_of_this_week, when__lt=sunday_of_next_week): # all meetings this week
            print(meeting)
            t = date.today()
            if t.weekday() == 6 or t == meeting.when.date(): # if it's sunday or day of meeting
                for r in meeting.rsvps.all():
                    if r.response == 'N':
                        continue

                    if t == meeting.when.date():
                        when = "today"
                    else:
                        when = "this {0}".format(meeting.when.strftime("%A"))
                    body = message.format(
                        name=r.users_name,
                        when=when,
                        loc_name=meeting.where.name,
                        phone=meeting.where.phone,
                        email=meeting.where.email,
                        address=meeting.where.address
                        )

                    for topic in meeting.topics.all():
                        body += topic_message.format(
                            title=topic.title,
                            speaker=topic.presentors.all()[0].name,
                            description=topic.description
                            )

                    send_mail('ChiPy Meeting Reminder', body, settings.DEFAULT_FROM_EMAIL, [r.users_email]) 

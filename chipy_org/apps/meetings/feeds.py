from datetime import timedelta

from django_ical.views import ICalFeed

from .models import Meeting


class MeetingFeed(ICalFeed):
    """
    A iCal feed for meetings
    """

    product_id = "-//chipy.org//Meeting//EN"
    timezone = "CST"

    def items(self):
        return Meeting.objects.order_by("-when").all()

    def item_description(self, item):
        description = "RSVP at http://chipy.org\n\n"
        for topic in item.topics.all():
            presenter_name = "None Given"
            if topic.presenters.count() > 0:
                presenter_name = topic.presenters.all()[0].name

            description += f"{topic.title} by {presenter_name}\n{topic.description}\n\n"
        return description

    def item_link(self, item):
        return ""

    def item_location(self, item):
        if item.where:
            return item.where.address
        else:
            return "To be determined..."

    def item_start_datetime(self, item):
        return item.when

    def item_end_datetime(self, item):
        return item.when + timedelta(hours=1)

    def item_title(self, item):
        return "ChiPy Meeting"

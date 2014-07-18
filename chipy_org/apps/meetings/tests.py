import datetime

import libs.test_utils as test_utils
from .models import RSVP, Meeting, Venue

class MeetingsTest(test_utils.AuthenticatedTest):
    def test_unique_rsvp(self):
        """
        Tests the uniqueness constraints on the rsvp model
        """

        from django.core.exceptions import ValidationError
        
        test_venue = Venue.objects.create(name = 'Test')
        meeting = Meeting.objects.create(when = datetime.date.today(),
                                         where = test_venue,

        )
        rsvp = RSVP.objects.create(user = self.user,
                                   meeting = meeting,
                                   response = 'Y',
        )

        with self.assertRaises(ValidationError):
            # RSVP needs to have a user or name
            rsvp_no_user = RSVP.objects.create(meeting = meeting,
                                               response = 'Y',
            )
            
        with self.assertRaises(ValidationError):
            # This should already exist
            duplicate_rsvp = RSVP.objects.create(user = self.user,
                                                 meeting = meeting,
                                                 response = 'Y',
            )


        with self.assertRaises(ValidationError):
            name_rsvp = RSVP.objects.create(name = 'Test Name',
                                            meeting = meeting,
                                            response = 'Y',
            )

            # Can't have two of the same name
            duplicate_name_rsvp = RSVP.objects.create(name = 'Test Name',
                                                      meeting = meeting,
                                                      response = 'Y',
            )

            


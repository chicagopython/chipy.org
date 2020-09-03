import logging

from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_email_to_admin_after_create_job_post(position, company, recipients):
    try:
        subject = "ChiPy: New Job Post Created"

        msg = (
            f"A new job post has been submitted for '{position} at {company}'."
            " Please review it for approval."
        )

        from_email = "DoNotReply@chipy.org"

        to_email = recipients

        send_mail(subject, msg, from_email, to_email)

    except Exception as e:
        logger.exception(e)


def send_email_to_admin_after_user_deletes_job_post(position, company, recipients):
    """If the user deletes the job post before the admin has a chance to review it,
       an email is sent to the admin notifying them of this. This way the
       admin knows that they don't have to look for the post as it no longer exists.
    """
    try:
        subject = "ChiPy: User Has Deleted Job Post"

        msg = (
            f"The job post for '{position} at {company}' has been deleted by the user."
            " You no longer have to review it."
        )

        from_email = "DoNotReply@chipy.org"

        to_email = recipients

        send_mail(subject, msg, from_email, to_email)

    except Exception as e:
        logger.exception(e)

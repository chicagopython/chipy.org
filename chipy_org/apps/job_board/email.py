import logging

from django.core.mail import send_mail

logger = logging.getLogger(__name__)

def send_email_to_admin_after_new_job_post(position, company, recipients):
    try:
        subject = "ChiPy: New Job Board Post"
        
        msg = (
            f"A new job post has been submitted for '{{position}} at {{company}}'."
            "Please review it for approval."
            )
        
        from_email = "DoNotReply@chipy.org"
        
        to_email = recipients

        send_mail(subject, msg, from_email, to_email)
    
    except Exception as e:
        logger.exception(e)
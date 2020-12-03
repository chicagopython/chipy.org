import datetime

from ..models import JobPost


def test_job_post_unexpired_posts_includes_recent_only(job_post):
    job_post.is_sponsor = True
    job_post.approve()

    # Create another
    job_post.pk = None
    job_post.approval_date = datetime.datetime(1994, 3, 1)
    job_post.save()

    assert JobPost.objects.count() == 2
    assert JobPost.unexpired_posts().count() == 1

import pytest
from django.urls import reverse
from django.test import override_settings
from django.conf import global_settings
from django.contrib.auth.models import User
from chipy_org.apps.job_board.models import JobPost


@pytest.mark.django_db
@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_job_board_url_create_update_delete(client):

    # browse to job board site
    response = client.get(reverse("job-board"))
    assert response.status_code == 200

    # should not be able to hit create/update/delete views without login
    response = client.get(reverse("create-job-post"), follow=True)
    assert response.status_code == 200

    # creat a job posting
    jp = JobPost(
        company_name="test-company",
        position="test-position",
        description="test-description",
        is_sponsor=False,
        can_host_meeting=False,
        status="SU",
        days_to_expire=10,
        company_website="www.google.com",
        agree_to_terms=True,
        is_from_recruiting_agency=False,
    )
    jp.save()

    # cannot view before approval
    response = client.get(reverse("job-post-detail", kwargs={"pk": jp.id}), follow=True)
    assert response.status_code == 404

    # should request a user login
    response = client.get(reverse("update-job-post", kwargs={"pk": jp.id}), follow=True)
    assert response.status_code == 200
    assert b"Sign in with" in response.content

    # should request a user login
    response = client.get(reverse("delete-job-post", kwargs={"pk": jp.id}), follow=True)
    assert response.status_code == 200
    assert b"Sign in with" in response.content

    # create a user and login
    user = User.objects.get_or_create(username="test_user")[0]
    client.force_login(user)

    # browse to create a job url
    response = client.get(reverse("create-job-post"))
    assert response.status_code == 200
    assert b"Create a Job Post" in response.content

    # make the user own the job posting
    jp.contact = user
    jp.save()

    # browse to update job
    response = client.get(reverse("update-job-post", kwargs={"pk": jp.pk}))
    assert response.status_code == 200
    assert b"test-company" in response.content
    assert b"test-position" in response.content
    assert b"test-description" in response.content

    # verifiy the job does not appear on the job board or details views
    response = client.get(reverse("job-board"))
    assert response.status_code == 200
    assert b"test-company" not in response.content
    assert b"test-position" not in response.content

    response = client.get(reverse("job-post-detail", kwargs={"pk": jp.id}))
    assert response.status_code == 404

    # verifiy the job appears on the job board and in the details views after approved

    # approve the job
    jp.status = "AP"
    jp.save()

    response = client.get(reverse("job-board"))
    assert response.status_code == 200
    assert b"test-company" in response.content
    assert b"test-position" in response.content

    response = client.get(reverse("job-post-detail", kwargs={"pk": jp.id}))
    assert response.status_code == 200
    assert b"test-company" in response.content
    assert b"test-position" in response.content
    assert b"test-description" in response.content

    # delete the job from the job board
    JobPost.objects.get(pk=jp.id).delete()

    response = client.get(reverse("job-board"))
    assert response.status_code == 200
    assert b"test-company" not in response.content
    assert b"test-position" not in response.content

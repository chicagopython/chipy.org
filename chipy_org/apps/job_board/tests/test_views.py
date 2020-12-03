import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from chipy_org.apps.job_board.models import JobPost

# pylint: disable=redefined-outer-name


@pytest.fixture
def user():
    return User.objects.get_or_create(username="test_user")[0]


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def owned_job_post(job_post, user):
    job_post.contact = user
    job_post.save()
    return job_post


@pytest.fixture
def create_post_params():
    return {
        "first_name": "Some",
        "last_name": "Body",
        "email": "somebody@example.com",
        "is_from_recruiting_agency": "something",
        "company_name": "something",
        "position": "something",
        "job_type": "FT",
        "location": "CH",
        "description": "something",
        "is_sponsor": "something",
        "can_host_meeting": "something",
        "company_website": "something",
        "how_to_apply": "something",
        "agree_to_terms": "something",
    }


def test_index_view_renders(client):
    # browse to job board site
    response = client.get(reverse("job-board"))
    assert response.status_code == 200


def test_login_required_to_create_post(client, create_post_params):
    # should not be able to hit create/update/delete views without login
    response = client.get(reverse("create-job-post"), follow=True)
    assert response.status_code == 200
    assert b"Sign in with" in response.content

    response = client.post(reverse("create-job-post"), create_post_params, follow=True)
    assert response.status_code == 200
    assert b"Sign in with" in response.content

    assert JobPost.objects.count() == 0


@pytest.mark.parametrize("action", ["update-job-post", "delete-job-post"])
def test_login_required_to_modify_posts(action, client, job_post):
    response = client.get(reverse(action, kwargs={"pk": job_post.id}), follow=True)
    assert response.status_code == 200
    assert b"Sign in with" in response.content


def test_can_get_create_form(authenticated_client):
    response = authenticated_client.get(reverse("create-job-post"))
    assert response.status_code == 200
    assert b"Create a Job Post" in response.content


def test_cannot_view_before_approval(client, job_post):
    response = client.get(reverse("job-post-detail", kwargs={"pk": job_post.id}), follow=True)
    assert response.status_code == 404


def test_can_create_job_post(authenticated_client, create_post_params):
    response = authenticated_client.post(reverse("create-job-post"), create_post_params)
    assert response.status_code == 302
    post = JobPost.objects.first()
    assert post.description == "something"


def test_user_can_update_job_post(authenticated_client, owned_job_post):
    response = authenticated_client.get(
        reverse("update-job-post", kwargs={"pk": owned_job_post.pk})
    )
    assert response.status_code == 200
    assert b"test-company" in response.content
    assert b"test-position" in response.content
    assert b"test-description" in response.content


def test_approved_job_posts_visible(client, job_post):
    # Not visible at first
    response = client.get(reverse("job-board"))
    assert b"test-company" not in response.content
    assert b"test-position" not in response.content

    response = client.get(reverse("job-post-detail", kwargs={"pk": job_post.id}))
    assert response.status_code == 404

    job_post.approve()

    response = client.get(reverse("job-board"))
    assert response.status_code == 200
    assert b"test-company" in response.content
    assert b"test-position" in response.content

    response = client.get(reverse("job-post-detail", kwargs={"pk": job_post.id}))
    assert response.status_code == 200
    assert b"test-company" in response.content
    assert b"test-position" in response.content
    assert b"test-description" in response.content

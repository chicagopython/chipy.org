from django.core import mail


def test_chipy_contact_view(client):
    assert len(mail.outbox) == 0
    response = client.post(
        "/contact/",
        {
            "sender": "test",
            "email": "test@test.com",
            "subject": "test subject",
            "message": "test message",
        },
    )
    assert response.status_code == 200
    assert len(mail.outbox) == 1

import pytest
import json
from unittest.mock import patch
from email_funcation import app  # Import the Flask mail API


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_mail_success(client):
    with patch("smtplib.SMTP") as mock_smtp:  # Mock SMTP
        payload = {
            "to": ["test@example.com"],
            "subject": "Test Subject",
            "body": "Test Email Body",
            "smtp_ip": "smtp.example.com",
            "smpt_port": 587,
            "from_name": "Sender Name",
            "from_email": "sender@example.com"
        }
        response = client.post("/", data=json.dumps(payload),
                               content_type="application/json")

        assert response.status_code == 200
        assert "Success Message" in response.json
        assert response.json["Success Message"] == "Mail Sent successfully"
        mock_smtp.assert_called()


def test_mail_missing_fields(client):
    payload = {"subject": "Test", "body": "Test"}  # Missing required fields
    response = client.post("/", data=json.dumps(payload),
                           content_type="application/json")

    assert response.status_code == 200
    assert "Error Message" in response.json
    assert "Missing parameters" in response.json["Error Message"]

from src.smtp.smtp_client import SMTPClient

def test_smtp_client_real_method():
    client = SMTPClient()
    result = client.send("Subject", "Body", "email@test.com")
    assert result is False
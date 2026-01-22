import pytest
from datetime import date
from src.account import Account
from src.smtp.smtp_client import SMTPClient

class TestAccountEmail:
    def test_send_history_success(self, mocker):
        account = Account("Jan", "Kowalski", "12345678901")
        account.historia = [100, -50]
        email = "jan@test.pl"
        
        mock_send = mocker.patch('src.smtp.smtp_client.SMTPClient.send', return_value=True)
        result = account.send_history_via_email(email)
        assert result is True
        
        mock_send.assert_called_once()
        
        args, _ = mock_send.call_args
        subject, body, addr = args
        
        today = date.today().strftime("%Y-%m-%d")
        assert subject == f"Account Transfer History {today}"
        assert f"Your history: [100, -50]" in body or str([100, -50]) in body
        assert addr == email

    def test_send_history_failure(self, mocker):
        account = Account("Jan", "Kowalski", "12345678901")
        mocker.patch('src.smtp.smtp_client.SMTPClient.send', return_value=False)
        
        result = account.send_history_via_email("jan@test.pl")
        
        assert result is False

    def test_send_history_company(self, mocker):
        from src.account import CompanyAccount
        account = CompanyAccount("Firma", "1234567890")
        account.historia = [-1775, 5000]
        mock_send = mocker.patch('src.smtp.smtp_client.SMTPClient.send', return_value=True)
        
        account.send_history_via_email("firma@test.pl")
        
        args, _ = mock_send.call_args
        body = args[1]
        assert "Company account history" in body
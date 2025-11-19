from src.account import CompanyAccount


class TestCompanyAccount:
    def test_company_account_creation(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        assert account.company_name == "Tech Corp"
        assert account.nip == "1234567890"
        assert account.balance == 0

    def test_company_account_nip_short(self):
        account = CompanyAccount("Tech Corp", "123456789")
        assert account.nip == "Invalid"

    def test_company_account_nip_long(self):
        account = CompanyAccount("Tech Corp", "12345678901")
        assert account.nip == "Invalid"

    def test_company_account_nip_letters(self):
        account = CompanyAccount("Tech Corp", "123456789A")
        assert account.nip == "Invalid"

    def test_company_account_no_promo(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        assert account.balance == 0

    def test_company_account_incoming_transfer(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.incoming_transfer(100)
        assert account.balance == 100

    def test_company_account_outgoing_transfer(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.incoming_transfer(200)
        account.outgoing_transfer(50)
        assert account.balance == 150

    def test_company_account_outgoing_transfer_insufficient(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.outgoing_transfer(50)
        assert account.balance == 0

    def test_company_account_multiple_transfers(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.incoming_transfer(100)
        account.incoming_transfer(50)
        account.outgoing_transfer(30)
        assert account.balance == 120

import pytest
from src.account import CompanyAccount

# Dodajemy dekorator, żeby mock działał w całej klasie
@pytest.mark.usefixtures("mock_nip_verification_global")
class TestCompanyAccount:
    def test_company_account_creation(self, company_account):
        assert company_account.company_name == "Tech Corp"
        assert company_account.nip == "1234567890"
        assert company_account.balance == 0

    @pytest.mark.parametrize("nip", ["123456789", "12345678901", "123456789A"])
    def test_company_account_invalid_nip(self, nip):
        # Tutaj musimy uważać - jeśli NIP jest niepoprawny długością, 
        # walidacja w gov.pl i tak się nie odpali (kod blokuje wcześniej),
        # więc mock nie jest konieczny, ale nie szkodzi.
        account = CompanyAccount("Tech Corp", nip)
        assert account.nip == "Invalid"

    def test_company_account_no_promo(self, company_account):
        assert company_account.balance == 0

    def test_company_account_incoming_transfer(self, company_account):
        company_account.incoming_transfer(100)
        assert company_account.balance == 100

    @pytest.mark.parametrize("initial,transfer,expected", [
        (200, 50, 150),
        (0, 50, 0),
    ])
    def test_company_account_outgoing_transfer(self, company_account, initial, transfer, expected):
        if initial > 0:
            company_account.incoming_transfer(initial)
        company_account.outgoing_transfer(transfer)
        assert company_account.balance == expected

    def test_company_account_multiple_transfers(self, company_account):
        company_account.incoming_transfer(100)
        company_account.incoming_transfer(50)
        company_account.outgoing_transfer(30)
        assert company_account.balance == 120

    @pytest.mark.parametrize("initial,transfer,expected", [
        (100, 50, 45),
        (55, 50, 0),
        (5, 0, 0),
        (0, 0, -5),
        (10, 50, 10),
    ])
    def test_express_outgoing_transfer_scenarios(self, company_account, initial, transfer, expected):
        if initial > 0:
            company_account.incoming_transfer(initial)
        company_account.express_outgoing_transfer(transfer)
        assert company_account.balance == expected

    def test_history_incoming_transfer(self, company_account):
        company_account.incoming_transfer(100)
        assert company_account.historia == [100]

    def test_history_express_transfer(self, company_account):
        company_account.incoming_transfer(100)
        company_account.express_outgoing_transfer(50)
        assert company_account.historia == [100, -50, -5]
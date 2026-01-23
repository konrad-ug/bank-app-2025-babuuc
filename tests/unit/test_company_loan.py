import pytest
from src.account import CompanyAccount

@pytest.mark.usefixtures("mock_nip_verification_global")
class TestCompanyLoan:
    @pytest.fixture
    def company_account(self):
        return CompanyAccount("Januszex", "1234567890")

    def test_company_loan_success(self, company_account):
        company_account.historia = [-1775, 10000]
        company_account.balance = 5000
        result = company_account.take_loan(2000)
        assert result is True
        assert company_account.balance == 7000

    def test_company_loan_fail_no_zus(self, company_account):
        company_account.historia = [5000, 5000] 
        company_account.balance = 10000
        result = company_account.take_loan(2000)
        assert result is False
        assert company_account.balance == 10000

    def test_company_loan_fail_insufficient_balance(self, company_account):
        company_account.historia = [-1775, 1000]
        company_account.balance = 100 
        result = company_account.take_loan(2000)
        assert result is False
        assert company_account.balance == 100
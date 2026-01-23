import pytest
from src.account import Account, CompanyAccount

@pytest.fixture
def personal_account():
    return Account("John", "Doe", "12345678901")

@pytest.fixture
def personal_account_born_1985():
    return Account("John", "Doe", "85012312345")

@pytest.fixture
def company_account(mock_nip_verification_global):
    return CompanyAccount("Tech Corp", "1234567890")

@pytest.fixture
def mock_nip_verification_global(mocker):
    return mocker.patch('src.account.CompanyAccount.verify_nip', return_value=True)
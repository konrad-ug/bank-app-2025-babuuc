import pytest
from src.account import Account, CompanyAccount


@pytest.fixture
def personal_account():
    return Account("John", "Doe", "12345678901")


@pytest.fixture
def personal_account_born_1985():
    return Account("John", "Doe", "85012312345")


@pytest.fixture
def company_account():
    return CompanyAccount("Tech Corp", "1234567890")

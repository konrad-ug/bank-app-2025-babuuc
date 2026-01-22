import pytest
from src.account import Account

class TestAccount:
    def test_account_creation(self, personal_account):
        assert personal_account.first_name == "John"
        assert personal_account.last_name == "Doe"
        assert personal_account.balance == 0
        assert personal_account.pesel == "12345678901"

    @pytest.mark.parametrize("pesel", ["123456789", "123456789012"])
    def test_account_creation_invalid_pesel_length(self, pesel):
        account = Account("John", "Doe", pesel)
        assert account.pesel == "Invalid"

    @pytest.mark.parametrize("promo_code,expected_balance", [
        ("PROM_ABC", 50),
        ("PROM_123", 50),
    ])
    def test_account_creation_valid_promo(self, promo_code, expected_balance):
        account = Account("John", "Doe", "12345678901", promo_code)
        assert account.balance == expected_balance

    @pytest.mark.parametrize("promo_code", [None, "", "PROMO_ABC", "PROMABC", "PROM_"])
    def test_account_creation_invalid_promo(self, personal_account, promo_code):
        account = Account("John", "Doe", "12345678901", promo_code)
        assert account.balance == 0

    @pytest.mark.parametrize("pesel,promo,expected", [
        ("85012312345", "PROM_ABC", 50),
        ("61012312345", "PROM_ABC", 50),
        ("60012312345", "PROM_ABC", 0),
        ("55012312345", "PROM_ABC", 0),
    ])
    def test_account_creation_birth_year(self, pesel, promo, expected):
        account = Account("John", "Doe", pesel, promo)
        assert account.balance == expected

    @pytest.mark.parametrize("pesel", ["123", "6101231234A"])
    def test_account_creation_invalid_pesel_data(self, pesel):
        account = Account("John", "Doe", pesel, "PROM_ABC")
        assert account.balance == 0

    def test_account_creation_promo_not_string(self, personal_account_born_1985):
        account = Account("John", "Doe", "85012312345", 12345)
        assert account.balance == 0

    @pytest.mark.parametrize("pesel,expected", [
        ("00212312345", 50), # 2000
        ("00412312345", 50), # 2100
        ("00612312345", 50), # 2200
        ("00812312345", 0),  # 1800
    ])
    def test_account_creation_different_centuries(self, pesel, expected):
        account = Account("John", "Doe", pesel, "PROM_ABC")
        assert account.balance == expected
    
    def test_account_pesel_non_digit(self):
        account = Account("John", "Doe", "1234567890a")
        assert account._extract_birth_year() is None
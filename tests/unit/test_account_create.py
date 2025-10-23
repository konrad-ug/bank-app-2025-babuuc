from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678901"

    def test_account_creation_short_pesel(self):
        account = Account("John", "Doe", "123456789")
        assert account.pesel == "Invalid"

    def test_account_creation_long_pesel(self):
        account = Account("John", "Doe", "123456789012")
        assert account.pesel == "Invalid"

    def test_account_creation_with_valid_promo_code(self):
        account = Account("John", "Doe", "12345678901", "PROM_ABC")
        assert account.balance == 50

    def test_account_creation_with_valid_promo_code_different_suffix(self):
        account = Account("John", "Doe", "12345678901", "PROM_123")
        assert account.balance == 50

    def test_account_creation_without_promo_code(self):
        account = Account("John", "Doe", "12345678901")
        assert account.balance == 0

    def test_account_creation_with_none_promo_code(self):
        account = Account("John", "Doe", "12345678901", None)
        assert account.balance == 0

    def test_account_creation_with_invalid_promo_code_wrong_prefix(self):
        account = Account("John", "Doe", "12345678901", "PROMO_ABC")
        assert account.balance == 0

    def test_account_creation_with_invalid_promo_code_no_underscore(self):
        account = Account("John", "Doe", "12345678901", "PROMABC")
        assert account.balance == 0

    def test_account_creation_with_invalid_promo_code_only_prom(self):
        account = Account("John", "Doe", "12345678901", "PROM_")
        assert account.balance == 0

    def test_account_creation_with_invalid_promo_code_empty_string(self):
        account = Account("John", "Doe", "12345678901", "")
        assert account.balance == 0

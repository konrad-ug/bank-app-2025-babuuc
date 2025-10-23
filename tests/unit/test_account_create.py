from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678901"

    def test_account_creation_shortpesel(self):
        account = Account("John", "Doe", "123456789")
        assert account.pesel == "Invalid"

    def test_account_creation_longpesel(self):
        account = Account("John", "Doe", "123456789012")
        assert account.pesel == "Invalid"

    def test_account_creation_promovalid(self):
        account = Account("John", "Doe", "12345678901", "PROM_ABC")
        assert account.balance == 50

    def test_account_creation_promosuf(self):
        account = Account("John", "Doe", "12345678901", "PROM_123")
        assert account.balance == 50

    def test_account_creation_nopromo(self):
        account = Account("John", "Doe", "12345678901")
        assert account.balance == 0

    def test_account_creation_nonepromo(self):
        account = Account("John", "Doe", "12345678901", None)
        assert account.balance == 0

    def test_account_creation_promowrong(self):
        account = Account("John", "Doe", "12345678901", "PROMO_ABC")
        assert account.balance == 0

    def test_account_creation_nounder(self):
        account = Account("John", "Doe", "12345678901", "PROMABC")
        assert account.balance == 0

    def test_account_creation_promoonly(self):
        account = Account("John", "Doe", "12345678901", "PROM_")
        assert account.balance == 0

    def test_account_creation_promoempty(self):
        account = Account("John", "Doe", "12345678901", "")
        assert account.balance == 0

    def test_account_creation_born85(self):
        account = Account("John", "Doe", "85012312345", "PROM_ABC")
        assert account.balance == 50

    def test_account_creation_born61(self):
        account = Account("John", "Doe", "61012312345", "PROM_ABC")
        assert account.balance == 50

    def test_account_creation_born60(self):
        account = Account("John", "Doe", "60012312345", "PROM_ABC")
        assert account.balance == 0

    def test_account_creation_born55(self):
        account = Account("John", "Doe", "55012312345", "PROM_ABC")
        assert account.balance == 0

    def test_account_creation_invalidpesel(self):
        account = Account("John", "Doe", "123", "PROM_ABC")
        assert account.balance == 0
        account = Account("John", "Doe", "123", "PROM_ABC")
        assert account.balance == 0

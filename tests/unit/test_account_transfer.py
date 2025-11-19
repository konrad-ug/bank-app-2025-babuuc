from src.account import Account


class TestAccountTransfer:
    def test_incoming_transfer(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        assert account.balance == 100

    def test_outgoing_transfer_sufficient_funds(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(200)
        account.outgoing_transfer(50)
        assert account.balance == 150

    def test_outgoing_transfer_insufficient_funds(self):
        account = Account("John", "Doe", "12345678901")
        account.outgoing_transfer(50)
        assert account.balance == 0

    def test_multiple_transfers(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        account.incoming_transfer(50)
        account.outgoing_transfer(30)
        assert account.balance == 120

    def test_outgoing_transfer_exact_balance(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        account.outgoing_transfer(100)
        assert account.balance == 0

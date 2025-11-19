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

    def test_express_outgoing_transfer_sufficient_funds(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        account.express_outgoing_transfer(50)
        assert account.balance == 49

    def test_express_outgoing_transfer_with_fee_only(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(1)
        account.express_outgoing_transfer(0)
        assert account.balance == 0

    def test_express_outgoing_transfer_below_zero_by_fee(self):
        account = Account("John", "Doe", "12345678901")
        account.express_outgoing_transfer(0)
        assert account.balance == -1

    def test_express_outgoing_transfer_insufficient_for_amount(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(10)
        account.express_outgoing_transfer(50)
        assert account.balance == 10

    def test_express_outgoing_transfer_exact_amount_plus_fee(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(51)
        account.express_outgoing_transfer(50)
        assert account.balance == 0

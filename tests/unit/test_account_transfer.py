import pytest
from src.account import Account


class TestAccountTransfer:
    def test_incoming_transfer(self, personal_account):
        personal_account.incoming_transfer(100)
        assert personal_account.balance == 100

    @pytest.mark.parametrize("initial,transfer,expected", [
        (200, 50, 150),
        (100, 100, 0),
    ])
    def test_outgoing_transfer_sufficient_funds(self, personal_account, initial, transfer, expected):
        personal_account.incoming_transfer(initial)
        personal_account.outgoing_transfer(transfer)
        assert personal_account.balance == expected

    def test_outgoing_transfer_insufficient_funds(self, personal_account):
        personal_account.outgoing_transfer(50)
        assert personal_account.balance == 0

    def test_multiple_transfers(self, personal_account):
        personal_account.incoming_transfer(100)
        personal_account.incoming_transfer(50)
        personal_account.outgoing_transfer(30)
        assert personal_account.balance == 120

    @pytest.mark.parametrize("initial,transfer,expected", [
        (100, 50, 49),
        (51, 50, 0),
    ])
    def test_express_outgoing_transfer_sufficient(self, personal_account, initial, transfer, expected):
        personal_account.incoming_transfer(initial)
        personal_account.express_outgoing_transfer(transfer)
        assert personal_account.balance == expected

    def test_express_outgoing_transfer_with_fee_only(self, personal_account):
        personal_account.incoming_transfer(1)
        personal_account.express_outgoing_transfer(0)
        assert personal_account.balance == 0

    def test_express_outgoing_transfer_below_zero_by_fee(self, personal_account):
        personal_account.express_outgoing_transfer(0)
        assert personal_account.balance == -1

    def test_express_outgoing_transfer_insufficient_for_amount(self, personal_account):
        personal_account.incoming_transfer(10)
        personal_account.express_outgoing_transfer(50)
        assert personal_account.balance == 10

    def test_history_incoming_transfer(self, personal_account):
        personal_account.incoming_transfer(100)
        assert personal_account.historia == [100]

    def test_history_outgoing_transfer(self, personal_account):
        personal_account.incoming_transfer(200)
        personal_account.outgoing_transfer(50)
        assert personal_account.historia == [200, -50]

    def test_history_express_transfer(self, personal_account):
        personal_account.incoming_transfer(500)
        personal_account.express_outgoing_transfer(300)
        assert personal_account.historia == [500, -300, -1]

    def test_history_multiple_transfers(self, personal_account):
        personal_account.incoming_transfer(100)
        personal_account.incoming_transfer(50)
        personal_account.outgoing_transfer(30)
        assert personal_account.historia == [100, 50, -30]

    @pytest.mark.parametrize("setup_func,expected_historia", [
        (lambda acc: acc.outgoing_transfer(50), []),
        (lambda acc: (acc.incoming_transfer(10), acc.express_outgoing_transfer(50)), [10]),
    ])
    def test_history_failed_transfers(self, personal_account, setup_func, expected_historia):
        setup_func(personal_account)
        assert personal_account.historia == expected_historia

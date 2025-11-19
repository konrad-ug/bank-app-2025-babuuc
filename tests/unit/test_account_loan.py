import pytest
from src.account import Account


class TestAccountLoan:
    @pytest.mark.parametrize("transfers,loan_amount,expected_result,expected_balance", [
        ([(100, "in"), (50, "in"), (30, "in")], 200, True, 380),
        ([(10, "in"), (20, "in"), (30, "in")], 100, True, 160),
        ([(-10, "out"), (100, "in"), (50, "in"), (30, "in")], 200, True, 380),
    ])
    def test_loan_last_three_incoming_success(self, personal_account, transfers, loan_amount, expected_result, expected_balance):
        for amount, transfer_type in transfers:
            if transfer_type == "in":
                personal_account.incoming_transfer(amount)
            elif transfer_type == "out":
                personal_account.outgoing_transfer(abs(amount))
        
        result = personal_account.submit_for_loan(loan_amount)
        assert result is expected_result
        assert personal_account.balance == expected_balance

    @pytest.mark.parametrize("transfers,loan_amount,expected_balance", [
        ([(100, "in"), (50, "in"), (20, "out")], 200, 130),
        ([(100, "in"), (50, "in"), (10, "express")], 50, 139),
    ])
    def test_loan_last_three_not_all_incoming(self, personal_account, transfers, loan_amount, expected_balance):
        for amount, transfer_type in transfers:
            if transfer_type == "in":
                personal_account.incoming_transfer(amount)
            elif transfer_type == "out":
                personal_account.outgoing_transfer(amount)
            elif transfer_type == "express":
                personal_account.express_outgoing_transfer(amount)
        
        result = personal_account.submit_for_loan(loan_amount)
        assert result is False
        assert personal_account.balance == expected_balance

    @pytest.mark.parametrize("transfers,loan_amount,expected_result,expected_balance", [
        ([(100, "in"), (50, "in"), (20, "out"), (80, "in"), (40, "in")], 200, True, 450),
        ([(60, "in"), (60, "in"), (60, "in"), (60, "in"), (61, "in")], 300, True, 601),
        ([(100, "in"), (50, "in"), (20, "out"), (40, "in"), (30, "in")], 200, False, 200),
        ([(100, "in"), (50, "in"), (60, "out"), (40, "in"), (30, "in")], 200, False, 160),
    ])
    def test_loan_sum_of_last_five(self, personal_account, transfers, loan_amount, expected_result, expected_balance):
        for amount, transfer_type in transfers:
            if transfer_type == "in":
                personal_account.incoming_transfer(amount)
            elif transfer_type == "out":
                personal_account.outgoing_transfer(amount)
        
        result = personal_account.submit_for_loan(loan_amount)
        assert result is expected_result
        assert personal_account.balance == expected_balance

    def test_loan_less_than_five_transactions(self, personal_account):
        personal_account.incoming_transfer(100)
        personal_account.incoming_transfer(50)
        personal_account.outgoing_transfer(20)
        result = personal_account.submit_for_loan(200)
        assert result is False
        assert personal_account.balance == 130

    def test_loan_express_transfer_counts_as_two(self, personal_account):
        personal_account.incoming_transfer(100)
        personal_account.incoming_transfer(50)
        personal_account.express_outgoing_transfer(20)
        result = personal_account.submit_for_loan(200)
        assert result is False
        assert personal_account.balance == 129

    def test_loan_no_transactions(self, personal_account):
        result = personal_account.submit_for_loan(100)
        assert result is False
        assert personal_account.balance == 0

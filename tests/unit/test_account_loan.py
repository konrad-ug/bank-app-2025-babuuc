from src.account import Account


class TestAccountLoan:
    def test_loan_last_three_incoming(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        account.incoming_transfer(50)
        account.incoming_transfer(30)
        result = account.submit_for_loan(200)
        assert result is True
        assert account.balance == 180

    def test_loan_last_three_not_all_incoming(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        account.incoming_transfer(50)
        account.outgoing_transfer(20)
        result = account.submit_for_loan(200)
        assert result is False
        assert account.balance == 130

    def test_loan_sum_of_last_five_greater(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        account.incoming_transfer(50)
        account.outgoing_transfer(20)
        account.incoming_transfer(80)
        account.incoming_transfer(40)
        result = account.submit_for_loan(200)
        assert result is True
        assert account.balance == 450

    def test_loan_sum_of_last_five_equal(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        account.incoming_transfer(50)
        account.outgoing_transfer(20)
        account.incoming_transfer(40)
        account.incoming_transfer(30)
        result = account.submit_for_loan(200)
        assert result is False
        assert account.balance == 200

    def test_loan_sum_of_last_five_less(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        account.incoming_transfer(50)
        account.outgoing_transfer(60)
        account.incoming_transfer(40)
        account.incoming_transfer(30)
        result = account.submit_for_loan(200)
        assert result is False
        assert account.balance == 160

    def test_loan_less_than_five_transactions(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        account.incoming_transfer(50)
        account.outgoing_transfer(20)
        result = account.submit_for_loan(200)
        assert result is False
        assert account.balance == 130

    def test_loan_express_transfer_counts_as_two(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        account.incoming_transfer(50)
        account.express_outgoing_transfer(20)
        result = account.submit_for_loan(200)
        assert result is False
        assert account.balance == 129

    def test_loan_exactly_three_incoming(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(10)
        account.incoming_transfer(20)
        account.incoming_transfer(30)
        result = account.submit_for_loan(100)
        assert result is True
        assert account.balance == 160

    def test_loan_more_than_three_last_three_incoming(self):
        account = Account("John", "Doe", "12345678901")
        account.outgoing_transfer(10)
        account.incoming_transfer(100)
        account.incoming_transfer(50)
        account.incoming_transfer(30)
        result = account.submit_for_loan(200)
        assert result is True
        assert account.balance == 370

    def test_loan_five_transactions_sum_check(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(60)
        account.incoming_transfer(60)
        account.incoming_transfer(60)
        account.incoming_transfer(60)
        account.incoming_transfer(61)
        result = account.submit_for_loan(300)
        assert result is True
        assert account.balance == 601

    def test_loan_express_fee_in_last_three(self):
        account = Account("John", "Doe", "12345678901")
        account.incoming_transfer(100)
        account.incoming_transfer(50)
        account.express_outgoing_transfer(10)
        result = account.submit_for_loan(50)
        assert result is False
        assert account.balance == 139

    def test_loan_no_transactions(self):
        account = Account("John", "Doe", "12345678901")
        result = account.submit_for_loan(100)
        assert result is False
        assert account.balance == 0

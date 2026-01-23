from src.account import Account

class AccountRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: Account):
        self.accounts.append(account)

    def get_account_by_pesel(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def get_count(self):
        return len(self.accounts)
    
    def delete_account(self, pesel):
        for i, account in enumerate(self.accounts):
            if account.pesel == pesel:
                del self.accounts[i]
                return True
        return False
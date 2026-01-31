import pytest
from src.account_registry import AccountRegistry
from src.account import Account

class TestAccountRegistry:
    @pytest.fixture
    def registry(self):
        return AccountRegistry()

    @pytest.fixture
    def account(self):
        return Account("Jan", "Kowalski", "12345678901")

    def test_add_account(self, registry, account):
        registry.add_account(account)
        assert registry.get_count() == 1

    def test_get_account_by_pesel(self, registry, account):
        registry.add_account(account)
        found = registry.get_account_by_pesel("12345678901")
        assert found == account

    def test_get_account_by_pesel_not_found(self, registry):
        found = registry.get_account_by_pesel("99999999999")
        assert found is None

    def test_delete_account_success(self, registry, account):
        registry.add_account(account)
        result = registry.delete_account("12345678901")
        assert result is True
        assert registry.get_count() == 0

    def test_delete_account_failed(self, registry):
        result = registry.delete_account("99999999999")
        assert result is False
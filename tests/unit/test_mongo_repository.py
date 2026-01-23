import pytest
from src.mongo_repository import MongoAccountsRepository
from src.account import Account, CompanyAccount

class TestMongoRepository:
    def test_save_all(self, mocker):
        mock_client = mocker.patch('src.mongo_repository.MongoClient')
        mock_collection = mock_client.return_value.__getitem__.return_value.__getitem__.return_value
        
        repo = MongoAccountsRepository()
        account = Account("Jan", "Kowalski", "12345678901")
        repo.save_all([account])
        
        mock_collection.delete_many.assert_called_once_with({})
        mock_collection.insert_many.assert_called_once()
        args, _ = mock_collection.insert_many.call_args
        inserted_data = args[0]
        
        assert inserted_data[0]["pesel"] == "12345678901"
        assert inserted_data[0]["first_name"] == "Jan"

    def test_save_all_with_company_account(self, mocker):
        mock_client = mocker.patch('src.mongo_repository.MongoClient')
        mock_collection = mock_client.return_value.__getitem__.return_value.__getitem__.return_value
        mocker.patch('src.account.CompanyAccount.verify_nip', return_value=True)
        
        repo = MongoAccountsRepository()
        company = CompanyAccount("Januszex", "1234567890")
        company.balance = 5000
        company.historia = [-1775, 1000]
        repo.save_all([company])
        
        mock_collection.delete_many.assert_called_once_with({})
        mock_collection.insert_many.assert_called_once()
        args, _ = mock_collection.insert_many.call_args
        inserted_data = args[0]
        
        assert inserted_data[0]["type"] == "company"
        assert inserted_data[0]["company_name"] == "Januszex"
        assert inserted_data[0]["nip"] == "1234567890"
        assert inserted_data[0]["balance"] == 5000
        assert inserted_data[0]["history"] == [-1775, 1000]

    def test_load_all(self, mocker):
        mock_client = mocker.patch('src.mongo_repository.MongoClient')
        mock_collection = mock_client.return_value.__getitem__.return_value.__getitem__.return_value
        
        mock_collection.find.return_value = [
            {
                "type": "personal",
                "first_name": "Anna",
                "last_name": "Nowak",
                "pesel": "99999999999",
                "balance": 100,
                "history": [100]
            },
            {
                "type": "company",
                "company_name": "Drutex",
                "nip": "8461627563", 
                "balance": 5000,
                "history": []
            },
            {
                "type": "company",
                "company_name": "Mafia",
                "nip": "0000000000", 
                "balance": 9999,
                "history": []
            }
        ]
        
        mocker.patch('src.account.CompanyAccount.verify_nip', side_effect=[True, False])

        repo = MongoAccountsRepository()
        loaded_accounts = repo.load_all()
        
        assert len(loaded_accounts) == 3
        
        assert loaded_accounts[0].first_name == "Anna"
        assert isinstance(loaded_accounts[0], Account)
        
        assert loaded_accounts[1].company_name == "Drutex"
        assert isinstance(loaded_accounts[1], CompanyAccount)
        
        assert loaded_accounts[2].company_name == "Mafia"
        assert loaded_accounts[2].nip == "0000000000"
        assert isinstance(loaded_accounts[2], CompanyAccount)
import pytest
from src.mongo_repository import MongoAccountsRepository
from src.account import Account

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
            }
        ]
        
        repo = MongoAccountsRepository()
        loaded_accounts = repo.load_all()
        
        assert len(loaded_accounts) == 1
        assert loaded_accounts[0].first_name == "Anna"
        assert loaded_accounts[0].balance == 100
        assert isinstance(loaded_accounts[0], Account)
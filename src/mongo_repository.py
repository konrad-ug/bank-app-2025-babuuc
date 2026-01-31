from pymongo import MongoClient
from src.account import Account, CompanyAccount

class MongoAccountsRepository:
    def __init__(self, host="localhost", port=27017, db_name="bank_db", collection_name="accounts"):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_all(self, accounts):
        self.collection.delete_many({})
        
        data_to_insert = [account.to_dict() for account in accounts]
        
        if data_to_insert:
            self.collection.insert_many(data_to_insert)

    def load_all(self):
        accounts_data = self.collection.find({})
        accounts_objects = []

        for data in accounts_data:
            if data["type"] == "personal":
                acc = Account(data["first_name"], data["last_name"], data["pesel"])
                acc.balance = data["balance"]
                acc.historia = data["history"]
                accounts_objects.append(acc)
            elif data["type"] == "company":
                try:
                    acc = CompanyAccount(data["company_name"], data["nip"])
                except ValueError:
                    acc = CompanyAccount(data["company_name"], "Invalid") 
                    acc.nip = data["nip"]
                
                acc.balance = data["balance"]
                acc.historia = data["history"]
                accounts_objects.append(acc)
        
        return accounts_objects
from flask import Flask, request, jsonify
from src.account import Account
from src.account_registry import AccountRegistry

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Request data: {data}")
    
    try:
        account = Account(data["name"], data["surname"], data["pesel"])
        registry.add_account(account)
        return jsonify({"message": "Account created"}), 201
    except Exception as e:
        return jsonify({"message": f"Error creating account: {str(e)}"}), 400

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.accounts
    accounts_data = [
        {
            "name": acc.first_name, 
            "surname": acc.last_name, 
            "pesel": acc.pesel, 
            "balance": acc.balance
        } 
        for acc in accounts
    ]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    count = registry.get_count()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.get_account_by_pesel(pesel)
    if account:
        return jsonify({
            "name": account.first_name,
            "surname": account.last_name,
            "pesel": account.pesel,
            "balance": account.balance
        }), 200
    else:
        return jsonify({"message": "Account not found"}), 404

# to do labow 8 jak rozumiem
@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    return jsonify({"message": "Account deleted"}), 200
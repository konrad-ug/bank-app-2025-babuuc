from behave import *
import requests

@step('Account registry is empty')
def clear_registry(context):
    resp = requests.get(f"{context.base_url}/count")
    assert resp.json()["count"] == 0

@step('I create an account using name: "{name}", last name: "{surname}", pesel: "{pesel}"')
def create_account(context, name, surname, pesel):
    json_body = {
        "name": name,
        "surname": surname,
        "pesel": pesel
    }
    resp = requests.post(context.base_url, json=json_body)
    assert resp.status_code == 201

@step('Number of accounts in registry equals: "{count}"')
def check_count(context, count):
    resp = requests.get(f"{context.base_url}/count")
    assert resp.json()["count"] == int(count)

@step('Account with pesel "{pesel}" exists in registry')
def check_account_exists(context, pesel):
    resp = requests.get(f"{context.base_url}/{pesel}")
    assert resp.status_code == 200

@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_not_exists(context, pesel):
    resp = requests.get(f"{context.base_url}/{pesel}")
    assert resp.status_code == 404

@step('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    resp = requests.delete(f"{context.base_url}/{pesel}")
    assert resp.status_code == 200

@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_account(context, field, pesel, value):
    json_body = { field: value }
    resp = requests.patch(f"{context.base_url}/{pesel}", json=json_body)
    assert resp.status_code == 200

@step('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def check_field_value(context, pesel, field, value):
    resp = requests.get(f"{context.base_url}/{pesel}")
    data = resp.json()
    assert data[field] == value

@step('I make an incoming transfer of "{amount}" to account with pesel "{pesel}"')
def make_incoming_transfer(context, amount, pesel):
    json_body = {"amount": int(amount), "type": "incoming"}
    resp = requests.post(f"{context.base_url}/{pesel}/transfer", json=json_body)
    context.last_response = resp
    assert resp.status_code == 200

@step('I make an outgoing transfer of "{amount}" from account with pesel "{pesel}"')
def make_outgoing_transfer(context, amount, pesel):
    json_body = {"amount": int(amount), "type": "outgoing"}
    resp = requests.post(f"{context.base_url}/{pesel}/transfer", json=json_body)
    context.last_response = resp

@step('Account with pesel "{pesel}" has balance equal to "{balance}"')
def check_balance(context, pesel, balance):
    resp = requests.get(f"{context.base_url}/{pesel}")
    assert resp.status_code == 200
    assert resp.json()["balance"] == int(balance)

@step('Transfer fails with message "{message}"')
def check_transfer_fail_message(context, message):
    assert context.last_response.status_code == 422
    assert context.last_response.json()["message"] == message
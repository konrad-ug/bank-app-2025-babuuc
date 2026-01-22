import pytest
from src.account import CompanyAccount

def test_verify_nip_valid(mocker):
    mock_get = mocker.patch('src.account.requests.get')
    
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "result": {
            "subject": {
                "statusVat": "Czynny",
                "name": "Januszex"
            }
        }
    }

    account = CompanyAccount("Firma", "12345678901")
    account.nip = "1234567890" 
    
    assert account.verify_nip() is True

def test_verify_nip_exception(mocker):
    mocker.patch('src.account.requests.get', side_effect=Exception("Connection error"))
    account = CompanyAccount("Firma", "12345678901")
    account.nip = "1234567890"
    
    assert account.verify_nip() is False

def test_constructor_raises_error_when_nip_invalid(mocker):
    mocker.patch.object(CompanyAccount, 'verify_nip', return_value=False)

    with pytest.raises(ValueError, match="Company not registered"):
        CompanyAccount("Januszex", "1234567890")

def test_verify_nip_not_active(mocker):
    mock_get = mocker.patch('src.account.requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "result": {
            "subject": {
                "statusVat": "Zwolniony",
                "name": "Januszex"
            }
        }
    }
    
    account = CompanyAccount("Firma", "12345678901")
    account.nip = "1234567890"
    
    assert account.verify_nip() is False
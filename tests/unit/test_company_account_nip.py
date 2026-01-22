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

    # ten test nie wywola konstruktora bo konstruktor tez wola verify nip co jest problematyczne
    # dlatego w pdf sugeruja na jakich poziomach mozemy mockowac
    # najbezpieczniej jest zamockowac cala metode verify nip w innych testach
    # a tutaj przetestowac verify nip na sucho lub stworzyc obiekt w specyficzny sposob
    
    # obejscie problemu konstruktora na potrzeby testowania samej metody
    # 1 tworzymy obiekt z invalid nipem zeby pominal weryfikacje w init
    # 2 podmieniamy nip recznie
    account = CompanyAccount("Firma", "12345678901")
    account.nip = "1234567890" # ustawiamy poprawny na potrzeby testu
    
    assert account.verify_nip() is True

def test_constructor_raises_error_when_nip_invalid(mocker):
    # mockujemy verify_nip zeby zwracalo False
    # dzieki temu nie musimy mockowac requests.get testujemy tylko logike konstruktora
    mocker.patch.object(CompanyAccount, 'verify_nip', return_value=False)

    with pytest.raises(ValueError, match="Company not registered"):
        CompanyAccount("Januszex", "1234567890")
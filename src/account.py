import requests
import os
from src.smtp.smtp_client import SMTPClient
from datetime import date

class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if len(pesel) == 11 else "Invalid"
        self.balance = 0
        self.historia = []
        
        if (
            promo_code
            and isinstance(promo_code, str)
            and promo_code.startswith("PROM_")
            and len(promo_code) > 5
            and self._is_born_after_1960()
        ):
            self.balance += 50

    def _extract_birth_year(self):
        if self.pesel == "Invalid" or not isinstance(self.pesel, str) or len(self.pesel) != 11:
            return None
        if not self.pesel.isdigit():
            return None

        yy = int(self.pesel[0:2])
        mm = int(self.pesel[2:4])

        if 1 <= mm <= 12:
            return 1900 + yy
        elif 21 <= mm <= 32:
            return 2000 + yy
        elif 41 <= mm <= 52:
            return 2100 + yy
        elif 61 <= mm <= 72:
            return 2200 + yy
        elif 81 <= mm <= 92:
            return 1800 + yy

        return (1900 + yy) if yy >= 60 else (2000 + yy)

    def _is_born_after_1960(self):
        year = self._extract_birth_year()
        return year is not None and year >= 1961

    def incoming_transfer(self, amount):
        self.balance += amount
        self.historia.append(amount)

    def outgoing_transfer(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.historia.append(-amount)

    def express_outgoing_transfer(self, amount):
        fee = 1
        if self.balance >= amount:
            self.balance -= (amount + fee)
            self.historia.append(-amount)
            self.historia.append(-fee)

    def _check_last_three_incoming(self):
        if len(self.historia) < 3:
            return False
        last_three = self.historia[-3:]
        return all(transaction > 0 for transaction in last_three)

    def _check_sum_of_last_five(self, amount):
        if len(self.historia) < 5:
            return False
        last_five = self.historia[-5:]
        return sum(last_five) > amount

    def submit_for_loan(self, amount):
        if self._check_last_three_incoming():
            self.balance += amount
            return True
        
        if self._check_sum_of_last_five(amount):
            self.balance += amount
            return True
        
        return False
    
    def send_history_via_email(self, email_address):
        client = SMTPClient()
        today = date.today().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"
        
        content = f"Personal account history: {self.historia}"
        
        return client.send(subject, content, email_address)
    
    def to_dict(self):
        return {
            "type": "personal",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "pesel": self.pesel,
            "balance": self.balance,
            "history": self.historia
        }


class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if len(nip) == 10 and nip.isdigit() else "Invalid"
        self.balance = 0
        self.historia = []
        
        if self.nip != "Invalid":
             if not self.verify_nip():
                 raise ValueError("Company not registered")

    def verify_nip(self):
        base_url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        today = date.today().strftime("%Y-%m-%d")
        url = f"{base_url}/api/search/nip/{self.nip}?date={today}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                status = data.get("result", {}).get("subject", {}).get("statusVat")
                if status == "Czynny":
                    return True
            return False
        except Exception:
            return False

    def express_outgoing_transfer(self, amount):
        fee = 5
        if self.balance >= amount:
            self.balance -= (amount + fee)
            self.historia.append(-amount)
            self.historia.append(-fee)

    def take_loan(self, amount):
        if self.balance < 2 * amount:
            return False
        if -1775 not in self.historia:
            return False
        self.balance += amount
        return True
    
    def send_history_via_email(self, email_address):
        client = SMTPClient()
        today = date.today().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"
        
        content = f"Company account history: {self.historia}"
        
        return client.send(subject, content, email_address)
    
    def to_dict(self):
        return {
            "type": "company",
            "company_name": self.company_name,
            "nip": self.nip,
            "balance": self.balance,
            "history": self.historia
        }
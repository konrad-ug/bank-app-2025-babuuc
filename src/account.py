class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if len(pesel) == 11 else "Invalid"
        self.balance = 0
        
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

    def outgoing_transfer(self, amount):
        if self.balance >= amount:
            self.balance -= amount

    def express_outgoing_transfer(self, amount):
        fee = 1
        if self.balance >= amount:
            self.balance -= (amount + fee)


class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if len(nip) == 10 and nip.isdigit() else "Invalid"
        self.balance = 0

    def express_outgoing_transfer(self, amount):
        fee = 5
        if self.balance >= amount:
            self.balance -= (amount + fee)
class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if len(pesel) == 11 else "Invalid"
        self.balance = 0
        
        if (promo_code and promo_code.startswith("PROM_") and len(promo_code) > 5 
            and self._is_born_after_1960()):
            self.balance += 50

    def _is_born_after_1960(self):
        if self.pesel == "Invalid":
            return False
        
        year_digits = int(self.pesel[:2])
        if year_digits <= 60:
            year = 2000 + year_digits
        else:
            year = 1900 + year_digits
        return year > 1960
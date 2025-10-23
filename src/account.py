class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if len(pesel) == 11 else "Invalid"
        self.balance = 0
        
        if promo_code and promo_code.startswith("PROM_") and len(promo_code) > 5:
            self.balance += 50
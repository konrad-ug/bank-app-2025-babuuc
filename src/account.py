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
            century = 1900
        elif 21 <= mm <= 32:
            century = 2000
        elif 41 <= mm <= 52:
            century = 2100
        elif 61 <= mm <= 72:
            century = 2200
        elif 81 <= mm <= 92:
            century = 1800
        else:
            return None

        return century + yy

    def _is_born_after_1960(self):
        year = self._extract_birth_year()
        return year is not None and year >= 1961
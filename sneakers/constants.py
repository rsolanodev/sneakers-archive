class Brand:
    NIKE = "Nike"
    ADIDAS = "Adidas"
    REEBOK = "Reebok"
    PUMA = "Puma"
    JORDAN = "Jordan"
    CONVERSE = "Converse"
    VANS = "Vans"
    NEW_BALANCE = "New Balance"
    ASICS = "ASICS"
    AMIGO = "Amigo"

    @classmethod
    def all(cls):
        return [
            getattr(Brand, brand)
            for brand in dir(cls)
            if not brand.startswith("__") and not callable(getattr(Brand, brand))
        ]


class Color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

    def __init__(self, text: str, extra: str = "default"):
        self.text: str = text
        self.extra: str = extra

    def _as_default(self):
        return f"{self.BOLD}{self.text}{Color.END}"

    def _is_mandatory(self):
        return f"{self.RED}{self.BOLD}Mandatory!{Color.END} {self._as_default()}"

    def _as_success(self):
        return f"{self.GREEN}{self._as_default()}"

    def _as_danger(self):
        return f"{self.RED}{self._as_default()}"

    def _as_warning(self):
        return f"{self.YELLOW}{self._as_default()}"

    def __repr__(self):
        extra = {
            "default": self._as_default(),
            "mandatory": self._is_mandatory(),
            "success": self._as_success(),
            "danger": self._as_danger(),
            "warning": self._as_warning(),
        }
        return extra[self.extra]

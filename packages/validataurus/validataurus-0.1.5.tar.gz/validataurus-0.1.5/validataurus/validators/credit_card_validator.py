import re
from validataurus.validators.validator import Validator

class CreditCardValidator(Validator):
    """Validator for credit card numbers."""

    @property
    def is_valid(self) -> bool:
        """Check if the credit card number is valid."""
        # Remove spaces
        card_number = self.value.replace(" ", "")

        # Check format
        if not re.match(r"^\d{13,19}$", card_number):
            return False

        # Validate using the Luhn algorithm
        return self.luhn_algorithm(card_number)

    def luhn_algorithm(self, card_number: str) -> bool:
        """Implement the Luhn algorithm."""
        total = 0
        reverse_digits = card_number[::-1]

        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n

        return total % 10 == 0

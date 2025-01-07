import re
from validataurus.validators.validator import Validator

class PasswordValidator(Validator):
    """Validator for passwords."""

    @property
    def is_valid(self) -> bool:
        """Check if the password meets security requirements."""
        # Minimum length
        if len(self.value) < 8:
            return False

        # Regular expressions for password criteria
        has_upper = r'[A-Z]'
        has_lower = r'[a-z]'
        has_digit = r'[0-9]'
        has_special = r'[!@#$%^&*(),.?":{}|<>]'

        # Check each criterion
        return all(
            re.search(pattern, self.value)
            for pattern in [has_upper, has_lower, has_digit, has_special]
        )

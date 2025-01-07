import phonenumbers
from validataurus.validators.validator import Validator

class PhoneNumberValidator(Validator):
    """Validator for phone numbers."""

    @property
    def is_valid(self) -> bool:
        """Check if the phone number is valid."""
        try:
            # Parse the phone number
            parsed_number = phonenumbers.parse(self.value, None)
            # Check if the number is valid
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.NumberParseException:
            # Return False if parsing fails
            return False

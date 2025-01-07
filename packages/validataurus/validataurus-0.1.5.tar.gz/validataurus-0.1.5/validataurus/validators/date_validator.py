from datetime import datetime
from validataurus.validators.validator import Validator

class BirthDateValidator(Validator):
    """Validator for birth dates."""

    @property
    def is_valid(self) -> bool:
        """Check if the birth date is valid."""
        try:
            # Parse the date
            birth_date = datetime.strptime(self.value, "%Y-%m-%d")

            # Ensure the date is not in the future
            return birth_date <= datetime.now()
        except ValueError:
            # Return False if the format is invalid
            return False

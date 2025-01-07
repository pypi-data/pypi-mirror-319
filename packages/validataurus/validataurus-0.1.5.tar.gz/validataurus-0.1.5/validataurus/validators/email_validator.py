import re
from validataurus.validators.validator import Validator

class EmailValidator(Validator):
    """Validator for email addresses."""
    
    @property
    def is_valid(self) -> bool:
        """Check if the email address is valid."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, self.value))

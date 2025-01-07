class Validator:
    """Base class for all validators."""
    def __init__(self, value: str):
        self.value = value

    def validate(self) -> bool:
        """Validate the input value."""
        return self.is_valid

    @property
    def is_valid(self) -> bool:
        """Validation logic to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method")

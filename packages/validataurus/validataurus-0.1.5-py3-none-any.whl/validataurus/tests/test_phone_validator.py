import unittest
from validataurus.validators.phone_validator import PhoneNumberValidator

class TestPhoneNumberValidator(unittest.TestCase):
    def test_valid_phone_numbers(self):
        self.assertTrue(PhoneNumberValidator("+14155552671").is_valid)  # Valid US number
        self.assertTrue(PhoneNumberValidator("+33123456789").is_valid)  # Valid French number

    def test_invalid_phone_numbers(self):
        self.assertFalse(PhoneNumberValidator("12345").is_valid)  # Too short
        self.assertFalse(PhoneNumberValidator("+abcd123456").is_valid)  # Invalid characters
        self.assertFalse(PhoneNumberValidator("").is_valid)  # Empty string

if __name__ == "__main__":
    unittest.main()

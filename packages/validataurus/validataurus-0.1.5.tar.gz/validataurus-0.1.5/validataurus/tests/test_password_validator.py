import unittest
from validataurus.validators.password_validator import PasswordValidator

class TestPasswordValidator(unittest.TestCase):
    def test_strong_passwords(self):
        self.assertTrue(PasswordValidator("Str0ngP@ss!").is_valid)  # Strong password
        self.assertTrue(PasswordValidator("G00d@P4ssword123!").is_valid)  # Strong with numbers and special chars

    def test_weak_passwords(self):
        self.assertFalse(PasswordValidator("weakpass").is_valid)  # No uppercase, special, or digit
        self.assertFalse(PasswordValidator("NoNumbers!").is_valid)  # Missing digit
        self.assertFalse(PasswordValidator("12345678").is_valid)  # No letters
        self.assertFalse(PasswordValidator("Short1!").is_valid)  # Too short
        self.assertFalse(PasswordValidator("").is_valid)  # Empty string

if __name__ == "__main__":
    unittest.main()

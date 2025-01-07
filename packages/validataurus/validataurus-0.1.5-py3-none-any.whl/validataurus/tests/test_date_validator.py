import unittest
from validataurus.validators.date_validator import BirthDateValidator

class TestDateValidator(unittest.TestCase):
    def test_valid_birth_dates(self):
        self.assertTrue(BirthDateValidator("2000-01-01").validate())
        self.assertTrue(BirthDateValidator("1995-12-31").validate())

    def test_invalid_birth_dates(self):
        self.assertFalse(BirthDateValidator("3000-01-01").validate())  # Future date
        self.assertFalse(BirthDateValidator("not-a-date").validate())  # Invalid format
        self.assertFalse(BirthDateValidator("").validate())  # Empty string

if __name__ == "__main__":
    unittest.main()

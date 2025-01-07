import unittest
from validataurus.validators.credit_card_validator import CreditCardValidator

class TestCreditCardValidator(unittest.TestCase):
    def test_valid_credit_cards(self):
        self.assertTrue(CreditCardValidator("4539 1488 0343 6467").is_valid)  # Example Visa
        self.assertTrue(CreditCardValidator("6011 1111 1111 1117").is_valid)  # Example Discover

    def test_invalid_credit_cards(self):
        self.assertFalse(CreditCardValidator("1234 5678 9012 3456").is_valid)  # Fails Luhn
        self.assertFalse(CreditCardValidator("not-a-card-number").is_valid)  # Invalid format
        self.assertFalse(CreditCardValidator("").is_valid)  # Empty string

if __name__ == "__main__":
    unittest.main()

import unittest
from validataurus.validators.email_validator import EmailValidator

class TestEmailValidator(unittest.TestCase):
    def test_valid_email(self):
        self.assertTrue(EmailValidator("test@example.com").is_valid)
        self.assertTrue(EmailValidator("user.name+tag@domain.co").is_valid)
        self.assertTrue(EmailValidator("user_name@sub.domain.org").is_valid)

    def test_invalid_email(self):
        self.assertFalse(EmailValidator("plainaddress").is_valid)
        self.assertFalse(EmailValidator("missing@domain").is_valid)
        self.assertFalse(EmailValidator("@missingusername.com").is_valid)
        self.assertFalse(EmailValidator("username@.com").is_valid)

if __name__ == "__main__":
    unittest.main()

import unittest
from services.user_service import UserService, UsernameExistsError, InvalidPasswordError, PasswordConfirmationError, InvalidCredentialsError
from entities.user import User

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()
        self.test_user = User("test", "Test1234")

    def test_login_with_valid_username_and_password(self):
        user = self.user_service.login(self.test_user.username, self.test_user.password)

        self.assertEqual(user.username, self.test_user.username)

    def test_login_with_invalid_username_and_valid_password(self):
        self.assertRaises(InvalidCredentialsError, lambda: self.user_service.login("testtest", self.test_user.password))

    def test_login_with_valid_username_and_invalid_password(self):
        self.assertRaises(InvalidCredentialsError, lambda: self.user_service.login(self.test_user.username, "Test1111"))

    def test_create_already_existing_username(self):
        self.user_service.create_user(self.test_user.username, self.test_user.password, self.test_user.password)

        self.assertRaises(UsernameExistsError, lambda: self.user_service.create_user("test", "Newpassw0rd", "Newpassw0rd"))

    def test_create_username_with_too_short_password(self):
        self.assertRaises(InvalidPasswordError, lambda: self.user_service.create_user("username", "2Short", "2Short"))

    def test_create_username_with_no_capital_letter_in_password(self):
        self.assertRaises(InvalidPasswordError, lambda: self.user_service.create_user("username", "nocapital2", "nocapital2"))

    def test_create_username_with_no_number_in_password(self):
        self.assertRaises(InvalidPasswordError, lambda: self.user_service.create_user("username", "Nonumber", "Nonumber"))

    def test_create_username_with_not_matching_passwords(self):
        self.assertRaises(PasswordConfirmationError, lambda: self.user_service.create_user("username", "Test12345", "Test54321"))

    def test_get_current_user(self):
        user = self.user_service.login(self.test_user.username, self.test_user.password)

        self.assertEqual(self.user_service.get_current_user(), user)
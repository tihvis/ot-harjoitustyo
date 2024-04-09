import unittest
from services.user_service import user_service, UsernameExistsError, InvalidPasswordError, PasswordConfirmationError, InvalidCredentialsError
from repositories.user_repository import user_repository
from entities.user import User


class TestUserService(unittest.TestCase):
    def setUp(self):
        user_repository.delete_all()
        self.username = "test"
        self.password = "Test1234"

    def test_create_user_with_valid_credentials_succeeds_and_logs_in(self):
        user = user_service.create_user(
            self.username, self.password, self.password)

        self.assertEqual(user_service.get_current_user(), user)

    def test_login_with_valid_username_and_password(self):
        user = user_service.create_user(
            self.username, self.password, self.password)

        result = user_service.login(self.username, self.password)

        self.assertEqual(user.username, result.username)
        self.assertEqual(user.password, result.password)

    def test_login_with_invalid_username_and_valid_password(self):
        self.assertRaises(InvalidCredentialsError,
                          lambda: user_service.login("testtest", self.password))

    def test_login_with_valid_username_and_invalid_password(self):
        self.assertRaises(InvalidCredentialsError,
                          lambda: user_service.login(self.username, "Test1111"))

    def test_create_already_existing_username(self):
        user_service.create_user(self.username, self.password, self.password)

        self.assertRaises(UsernameExistsError, lambda: user_service.create_user(
            "test", "Newpassw0rd", "Newpassw0rd"))

    def test_create_username_with_too_short_password(self):
        self.assertRaises(InvalidCredentialsError, lambda: user_service.create_user(
            "username", "2Short", "2Short"))

    def test_create_username_with_no_capital_letter_in_password(self):
        self.assertRaises(InvalidPasswordError, lambda: user_service.create_user(
            "username", "nocapital2", "nocapital2"))

    def test_create_username_with_no_number_in_password(self):
        self.assertRaises(InvalidPasswordError, lambda: user_service.create_user(
            "username", "Nonumber", "Nonumber"))

    def test_create_username_with_not_matching_passwords(self):
        self.assertRaises(PasswordConfirmationError, lambda: user_service.create_user(
            "username", "Test12345", "Test54321"))

    def test_get_current_user(self):
        user = user_service.create_user(
            self.username, self.password, self.password)

        self.assertEqual(user_service.get_current_user(), user)

    def test_logout(self):
        user_service.create_user(self.username, self.password, self.password)

        user_service.logout()

        self.assertIsNone(user_service.get_current_user())

    def test_get_users(self):
        user1 = user_service.create_user(
            self.username, self.password, self.password)
        user2 = user_service.create_user(
            "second_user", self.password, self.password)
        user3 = user_service.create_user(
            "third_user", self.password, self.password)

        users = user_service.get_users()

        self.assertEqual(len(users), 3)
        self.assertEqual(users[0].username, user1.username)
        self.assertEqual(users[1].username, user2.username)
        self.assertEqual(users[2].username, user3.username)

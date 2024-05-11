import unittest
from repositories.user_repository import user_repository
from entities.user import User


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        user_repository.delete_all()
        self.user1 = User("test_user1", "P4ssw0rd", 1)
        self.user2 = User("test_user2", "S3cr3tpass", 2)

    def test_create(self):
        user = user_repository.create(self.user1)

        self.assertEqual(user.username, self.user1.username)
        self.assertEqual(user.password, self.user1.password)

    def test_find_all(self):
        user_repository.create(self.user1)
        user_repository.create(self.user2)
        users = user_repository.find_all()

        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].username, self.user1.username)
        self.assertEqual(users[1].username, self.user2.username)

    def test_find_by_username(self):
        user_repository.create(self.user1)

        user = user_repository.find_by_username(self.user1.username)

        self.assertEqual(user.username, self.user1.username)

    def test_delete_all(self):
        user_repository.create(self.user1)
        user_repository.create(self.user2)

        self.assertEqual(len(user_repository.find_all()), 2)

        user_repository.delete_all()

        self.assertEqual(len(user_repository.find_all()), 0)

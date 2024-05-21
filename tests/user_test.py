import unittest

from eqms.user import Role, User


class TestUsers(unittest.TestCase):
    def test_create_a_user(self):
        new_user = User(
            "Doe",
            surname="John",
            email="john.doe@example.com",
            roles=[Role.QA, Role.ADMIN, Role.ADMIN]
        )
        self.assertEqual(new_user.email, "john.doe@example.com")
        self.assertEqual(str(new_user), "John Doe")


if __name__ == '__main__':
    unittest.main()

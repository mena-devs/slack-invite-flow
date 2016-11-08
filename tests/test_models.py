import unittest

from slack_invite_flow import models


class MenaviteTests(unittest.TestCase):

    def build_user(self, first, last):
        return {first: {
            'first': first,
            'last': last,
            'email': '{}.{}@gmail.com'.format(first, last)
        }}

    def test_user_load(self):
        user = models.User.load(self.build_user('john', 'doe'))

        assert ['john', 'doe', 'john.doe@gmail.com'] == [
            user.first,
            user.last,
            user.email
        ]

    def test_user_load_exception(self):
        user = {}

        with self.assertRaises(models.ConfigurationException):
            models.User.load(user)

    def test_manager_load(self):
        users = models.UserManager.load([
            self.build_user('john', 'doe'),
            self.build_user('jane', 'smith'),
            self.build_user('foo', 'bar'),
            self.build_user('gee', 'see'),
        ])

        assert [
            ['john', 'john', 'doe', 'john.doe@gmail.com'],
            ['jane', 'jane', 'smith', 'jane.smith@gmail.com'],
            ['foo', 'foo', 'bar', 'foo.bar@gmail.com'],
            ['gee', 'gee', 'see', 'gee.see@gmail.com']] == users.as_table

    def test_manager_first_names(self):
        users = models.UserManager.load([
            self.build_user('john', 'doe'),
            self.build_user('jane', 'smith'),
            self.build_user('foo', 'bar'),
            self.build_user('gee', 'see'),
        ])

        assert 'john, jane, foo and gee' == users.first_names


if __name__ == '__main__':
    unittest.main()

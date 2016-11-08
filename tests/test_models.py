import pytest

from slack_invite_flow import models


def build_user(first, last):
    return {first: {
        'first': first,
        'last': last,
        'email': '{}.{}@gmail.com'.format(first, last)
    }}


def test_user_load():
    user = models.User.load(build_user('john', 'doe'))

    assert ['john', 'doe', 'john.doe@gmail.com'] == [
        user.first,
        user.last,
        user.email
    ]


def test_user_load_exception():
    user = {}

    with pytest.raises(models.ConfigurationException):
        models.User.load(user)


def test_manager_load():
    users = models.UserManager.load([
        build_user('john', 'doe'),
        build_user('jane', 'smith'),
        build_user('foo', 'bar'),
        build_user('gee', 'see'),
    ])

    assert [
        ['john', 'john', 'doe', 'john.doe@gmail.com'],
        ['jane', 'jane', 'smith', 'jane.smith@gmail.com'],
        ['foo', 'foo', 'bar', 'foo.bar@gmail.com'],
        ['gee', 'gee', 'see', 'gee.see@gmail.com']] == users.as_table


def test_manager_first_names():
    users = models.UserManager.load([
        build_user('john', 'doe'),
        build_user('jane', 'smith'),
        build_user('foo', 'bar'),
        build_user('gee', 'see'),
    ])

    assert 'john, jane, foo and gee' == users.first_names

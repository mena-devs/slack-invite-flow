class ConfigurationException(Exception):
    """Thrown during bad configurations"""
    pass


class User(object):
    """Holds details pertaining to a User"""

    def __init__(self, short, first, last, email):
        """Builds a user from a list of details"""
        self.short = short
        self.first = first
        self.last = last
        self.email = email

    @classmethod
    def load(cls, flat):
        """Builds a user from a dictionary"""
        try:
            short = flat.keys()[0]
            details = flat[short]
            return cls(
                short=short,
                first=details['first'],
                last=details['last'],
                email=details['email'])
        except (IndexError, KeyError):  # IndexError may be caught by yaml
            raise ConfigurationException(
                'Bad configuration for {}'.format(flat))

    @property
    def full_name(self):
        """Returns the user's full name"""
        return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        """Returns a string representation of a user object"""
        return '<User: {}>'.format(self.full_name)


class UserManager(list):
    """Container of users"""
    PLAIN_ENGLISH_TEMPLATE = "{} and {}"

    @property
    def first_names(self):
        """Returns the full names of all users as string"""
        _first_names = [user.first for user in self]
        all_except_last_user = _first_names[:-1]
        last_user = _first_names[-1]
        return self.PLAIN_ENGLISH_TEMPLATE.format(
            ', '.join(all_except_last_user),
            last_user)

    @property
    def emails(self):
        """Returns a list of all emails"""
        return [x.email for x in self]

    @classmethod
    def load(cls, flat):
        """Builds a user manager from a list of user details"""
        return cls([User.load(x) for x in flat])

    def __getitem__(self, key):
        """Retrieves a user by short name"""
        try:
            return [user for user in self if user.short == key][0]
        except IndexError:
            raise KeyError('No user with shortname "{}" found.'.format(key))

    @property
    def as_table(self):
        """Builds a table of flat details for all users"""
        return [[x.short, x.first, x.last, x.email] for x in self]

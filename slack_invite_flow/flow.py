"""Flow related logic"""

import abc
import collections
import datetime

import six


ActivityConfig = collections.namedtuple('ActivityConfig', 'kind extend repeat')
Log = collections.namedtuple('Log', 'when action error')


class FailedActivity(Exception):
    """Thrown when a state is incomplete"""
    pass


@six.add_metaclass(abc.ABCMeta)
class Activity(object):
    """Base state class"""

    @abc.abstractmethod
    def execute(self, payload):
        """abstract state execute function"""
        pass


class ActivityFlow(collections.OrderedDict):
    """Activity execution system"""

    def log(self, action):
        return Log(datetime.datetime.now(), action, '')

    def error(self, action, error):
        return Log(datetime.datetime.now(), action, error)

    def play(self, payload=None, initial=None):
        """Plays the activity configuration sequentially and incrementally
        spits out a log of the actions happening.

        If an `initial` state is passed, the flow will ignore earlier
        activities

        Activity configurations provide the following:

            Kind => Defines the activity class that holds the execution logic
            Extend => Defines whether the flow continues on activity error
            Repeat => Defines how many times the activity repeats on error
        """
        yield self.log('starting')
        skipped = False
        for name, configuration in self.items():

            # The following block handles the ability to skip activities
            if initial and initial != name and not skipped:
                yield self.log('skipping {}'.format(name))
                continue
            else:
                skipped = True

            instance = configuration.kind()

            # The following block handles execution and the ability to repeat
            repeat = False
            graceful = False
            for trial in range(configuration.repeat + 1):
                try:
                    yield self.log('playing {}{}'.format(
                        name, ' with repeat' if repeat else ''))
                    instance.execute(payload)
                    graceful = True
                    break
                except Exception as e:  # TODO: Enforce only FailedState?
                    yield self.error('error {}'.format(name), str(e))
                    repeat = True

            # The following block handles the ability to fallthrough on error
            if not graceful and not configuration.extend:
                break

        yield self.log('flow complete')

"""Flow related logic"""

import abc
import collections


ActivityConfig = collections.namedtuple('ActivityConfig', 'kind extend repeat')


class FailedActivity(Exception):
    """Thrown when a state is incomplete"""
    pass


class Activity(object):
    """Base state class"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self, payload):
        """abstract state execute function"""
        pass


class ActivityFlow(collections.OrderedDict):
    """Activity execution system"""

    # TODO: Make this yield or spit out a log instead of printing
    def play(self, payload, initial=None):
        """Plays the activity configuration sequentially.

        If an `initial` state is passed, the flow will ignore earlier
        activities

        Activity configurations provide the following:

            Kind => Defines the activity class that holds the execution logic
            Extend => Defines whether the flow continues on activity error
            Repeat => Defines how many times the activity repeats on error
        """
        print('Flow: Starting')
        skipped = False
        for name, configuration in self.items():

            # The following block handles the ability to skip activities
            if initial and initial != name and not skipped:
                print('Flow: Skipping {}'.format(name))
                continue
            else:
                skipped = True

            instance = configuration.kind()

            # The following block handles execution and the ability to repeat
            repeat = False
            graceful = False
            for trial in range(configuration.repeat + 1):
                try:
                    print('Flow: Playing {}{}'.format(
                        name, ' (REPEAT)' if repeat else ''))
                    instance.execute(payload)
                    graceful = True
                    break
                except Exception as e:
                    print('Flow: ERROR -> {}'.format(e))
                    repeat = True

            # The following block handles the ability to fallthrough on error
            if not graceful and not configuration.extend:
                break

        print('Flow: Complete')

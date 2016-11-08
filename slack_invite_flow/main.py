"""
Slack Invite Flow

Rudimentary workflow to automate slack team invitations
"""
import argparse
import sys

import yaml

import activities
import flow
import models


def request_user_stdin(key):
    return models.User(
        short=raw_input('[{}] short name: '.format(key)),
        first=raw_input('[{}] first name: '.format(key)),
        last=raw_input('[{}] last name: '.format(key)),
        email=raw_input('[{}] email: '.format(key)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', default='etc/config.yaml',
                        help='path to the config file')
    args = parser.parse_args()

    workflow = flow.ActivityFlow(
        inviter=flow.ActivityConfig(
            kind=activities.InviteUserToSlackTeam, extend=False, repeat=1),
        updater=flow.ActivityConfig(
            kind=activities.UpdateQuipMembersDocument, extend=True, repeat=1),
        notifier=flow.ActivityConfig(
            kind=activities.SendCodeOfConductEmail, extend=True, repeat=1))

    try:
        with open(args.config) as config_file:
            # TODO: Provide a _local_ web frontend.
            # See python module: webbrowser
            print 'MENA Devs Slack Invite - Automation'
            workflow.play(
                payload=dict(
                    config=yaml.load(config_file.read()),
                    from_user=raw_input('> admin short name: '),
                    to_user=request_user_stdin('who'),
                    referring_user=request_user_stdin('referrer')),
                initial='inviter')  # initial is optional left for demo
    except IOError:
        print("Cannot read config file {}".format(args.config))


if __name__ == '__main__':
    main()

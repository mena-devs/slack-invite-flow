# Slack Invite Flow

This project allows developers to build custom activities when plugged into
the flow machinery, would constitute a sequential workflow for inviting people
to slack.

## Installation

    pip install -r requirements.txt

## Configuration

The system requires some configuration and input in order for it to properly
run:

- [a configuration file](./config.yaml)
    - List of slack administrators required
    - Slack Token required
    - Quip Token required
    - Target Quip Document ID required
    - Mail settings required
- the user that is being invited
- the referring user
- the shortname of the admin as it appears in the configuration file

## How It Works

The workflow that is preconfigured is as follows and it is currently tuned
for [MENA Devs](https://mena-devs.slack.com) Slack Invitations:

    InviteUserToSlackTeam -> UpdateQuipMembersDocument -> SendCodeOfConductEmail

Each activity when plugged into the workflow machinery must also provide flags
that identify whether the activity can `fallthrough` on error or shortcircuit
if the activity fails to complete. Additionally the activity configuration must
provide a `repeat` flag that defines how many times the activity can repeat
before the flow machinery gives up (This can be helpful in case of credential
problems or connection problems, etc..)

By default the system comes with three built-in activities:

### InviteUserToSlackTeam

Uses the slack api in order to send an invitation to a user. The method used
by the system is an undocumented function call `users.admin.invite`

### UpdateQuipMembersDocument

Uses the quip api (locally imported, unavailable on pypi) in order to append
to a members document the details pertaining to the invitation. (as seen by
the `ROW_TEMPLATE`)

### SendCodeOfConductEmail

Uses `smtplib` and an imap server (defaults to `gmail` configuration) in order
to send a code of conduct email to the user. The mailer attaches two different
messages, one as plain text and the other as html, both configurable by a template
and within the configuration file itself.

# Sample Flow Run

    % python main.py
    MENA Devs Slack Invite - Automation
    > admin short name: dany
    [who] short name: john
    [who] first name: John
    [who] last name: Doe
    [who] email: john.doe@gmail.com
    [referrer] short name: jane
    [referrer] first name: Jane
    [referrer] last name: Smith
    [referrer] email: jane.smith@gmail.com
    Flow: Starting
    Flow: Playing inviter
    Flow: Playing updater
    Flow: Playing notifier
    Username: dany.stalone@gmail.com
    Password:
    Flow: Complete

# TODO

- the system is missing quite a bit of tests
- the system focuses on a CLI entry point, this doesn't have to be the case
- there are some `TODO` that needs handling (find them!)
...

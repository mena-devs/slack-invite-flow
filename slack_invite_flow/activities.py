import datetime
import email.mime.multipart
import email.mime.text
import getpass
import smtplib
import xml

import jinja2
import slackclient

import flow
import models
import quip


class SendCodeOfConductEmail(flow.Activity):
    """Menavite state that sends an email"""

    def execute(self, config, to_user, from_user, referring_user, **payload):
        """Sends a Code of Conduct by mail"""
        admins = models.UserManager.load(config['admins'])
        from_user = admins[from_user]

        with open(config['mailer']['templates']['plain']) as _file:
            plain = jinja2.Template(_file.read())

        with open(config['mailer']['templates']['html']) as _file:
            html = jinja2.Template(_file.read())

        plain_message = plain.render(
            admins=admins,
            from_user=from_user,
            to_user=to_user)

        html_message = html.render(
            admins=admins,
            from_user=from_user,
            to_user=to_user)

        self.sendmail(config,
                      to_user,
                      from_user,
                      referring_user,
                      admins,
                      plain_message,
                      html_message)

    # TODO: Args Attack! Refactor.
    def sendmail(self,
                 config,
                 to_user,
                 from_user,
                 referring_user,
                 admins,
                 plain_message,
                 html_message):
        """Sends an email given the configuration"""
        recipients = admins.emails + [referring_user.email, to_user.email]
        mime_message = email.mime.multipart.MIMEMultipart('alternative')
        mime_message['Subject'] = config['mailer']['subject']
        mime_message['To'] = to_user.email
        mime_message['Cc'] = referring_user.email
        mime_message['Bcc'] = ','.join(admins.emails)

        mime_message.attach(email.mime.text.MIMEText(plain_message, 'plain'))
        mime_message.attach(email.mime.text.MIMEText(html_message, 'html'))

        server = smtplib.SMTP(config['mailer']['server'])
        server.ehlo()
        server.starttls()
        server.login(
            raw_input('Username: '),
            getpass.getpass())
        server.sendmail(from_user.email, recipients, mime_message.as_string())
        server.quit()


class InviteUserToSlackTeam(flow.Activity):
    """Menavite state that invites to a slack team"""

    def execute(self, config, to_user, **payload):
        """Invites a user to slack"""
        token = config['services']['slack']['token']
        client = slackclient.SlackClient(token)

        result = client.api_call("users.admin.invite",
                                 email=to_user.email,
                                 first_name=to_user.first,
                                 last_name=to_user.last)

        if not result['ok']:
            raise flow.FailedActivity(
                "SlackInvite Error: {}".format(result['error']))


class UpdateQuipMembersDocument(flow.Activity):
    """Menavite state that updates the members in a quip document"""

    ROW_TEMPLATE = """
    <tr>
        <td><span>{{to_user.full_name}}</span></td>
        <td><span>{{to_user.email}}</span></td>
        <td><span>Company</span></td>
        <td><span>Title</span></td>
        <td><span>{{today}}</span></td>
        <td></td> <!-- I have no clue! if you omit this a column is lost! -->
        <td><span>{{from_user.first}}</span></td>
        <td><span>{{referring_user.full_name}}</span></td>
        <td><span>Yes</span></td> <!-- This should be calculated -->
    </tr>
    """

    def execute(self, config, to_user, from_user, referring_user, **payload):
        """Updates the quip members document"""
        admins = models.UserManager.load(config['admins'])
        from_user = admins[from_user]

        token = config['services']['quip']['token']
        client = quip.QuipClient(access_token=token)
        document_id = config['services']['quip']['document']

        last_row_id = self.fetch_last_row_id(client, document_id)
        new_row = self.build_new_row(
            to_user=to_user,
            from_user=from_user,
            referring_user=referring_user)

        client.edit_document(document_id,
                             new_row,
                             operation=quip.QuipClient.AFTER_SECTION,
                             section_id=last_row_id)

    def fetch_last_row_id(self, client, document_id):
        """Retrieves the id of the last row in the document"""
        document = client.get_thread(document_id)
        root = xml.etree.ElementTree.fromstring(
            '<root>{}</root>'.format(document['html']))  # etree fix

        # sup etree? why you no find tr without parents?
        return root.find('.//table/tbody/tr[last()]').attrib['id']

    def build_new_row(self, to_user, from_user, referring_user):
        """Creates a new html row <tr> from configuration"""
        template = jinja2.Template(self.ROW_TEMPLATE)
        today = datetime.datetime.strptime(
            str(datetime.datetime.today().date()),
            "%Y-%m-%d").strftime("%d/%m/%Y")
        return template.render(
            today=today,
            referring_user=referring_user,
            from_user=from_user,
            to_user=to_user)

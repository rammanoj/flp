from __future__ import print_function
from googleapiclient import discovery, errors
from httplib2 import Http
from oauth2client import file, client, tools
from flp.settings import STATIC_ROOT
from email.mime.text import MIMEText
from . import content
from .mail_template import mail_template
import base64


SEND_MAIL = 'rammanojpotla1608@gmail.com'
SCOPES = ['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.send']


def send_mail(service, to_mail, **kwargs):
    message = {}
    if kwargs['mail_type'] == 0:
        # user registration
        contents = content.registration['pre_message'] + content.registration['uri'] + kwargs['id'] + \
                   content.registration['post_message']
        contents = mail_template(content.registration['subject'], contents)
        message = MIMEText(contents, 'html')
        message['subject'] = content.registration['subject']
    elif kwargs['mail_type'] == 1:
        # Email change operation
        contents = content.email_change['pre_message'] + content.email_change['uri'] + kwargs['id'] + \
                   content.email_change['post_message']
        contents = mail_template(content.email_change['subject'], contents)
        message = MIMEText(contents, 'html')
        message['subject'] = content.email_change['subject']
    elif kwargs['mail_type'] == 2:
        # user forgot password
        contents = content.forgot_password['pre_message'] + content.forgot_password['uri'] + \
                  kwargs['id'] + content.forgot_password['post_message']
        contents = mail_template(content.forgot_password['subject'], contents)
        message = MIMEText(contents, 'html')
        message['subject'] = content.forgot_password['subject']

    elif kwargs['mail_type'] == 3:
        # Invite User to the group
        contents = content.invite['message'][0] + "<b>" + kwargs['team'] + "</b>. " + content.invite['message'][1] + \
                     kwargs['invitelink'] + content.invite['message'][2]
        contents = mail_template(content.invite['subject'], contents)
        message = MIMEText(contents, 'html')
        message['subject'] = content.invite['subject']
        message['bcc'] = "".join(i + "," for i in kwargs['bcc'])[:-1]
    elif kwargs['mail_type'] == 4:
        # Create a Post
        contents = content.new_post['message'][0] + "<b>" + kwargs['group'] + "</b>. " + content.new_post['message'][1] \
                   + "<b>" + kwargs['user'] + "</b>" + content.new_post['message'][2] + "<a " \
                    "href='" + kwargs['link'] + "' style='text-decoration: none;color:'#4d7ac1'>click here.</a>"
        contents = mail_template(content.new_post['subject'], contents)
        message = MIMEText(contents, 'html')
        message['subject'] = content.new_post['subject']
        message['bcc'] = "".join(i + "," for i in kwargs['bcc'])[:-1]
    elif kwargs['mail_type'] == 5:
        # Update the POST
        contents = content.update_psot['message'][0] + "<b>" + kwargs['post'] + "</b>. " + content.update_psot['message'][1] + \
                   "<b>" + kwargs['user'] + "</b>" + content.update_psot['message'][2] + "<b>" + kwargs['group'] + "</b>." \
            + "<a href='" + kwargs['link'] + "' style='text-decoration: none;color:'#4d7ac1'>Click here</a>" + content.update_psot['message'][3]
        contents = mail_template(content.invite['subject'], contents)
        message = MIMEText(contents, 'html')
        message['subject'] = content.update_psot['subject']
        message['bcc'] = "".join(i + "," for i in kwargs['bcc'])[:-1]

    message['to'] = to_mail
    message['from'] = SEND_MAIL

    msg = {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

    try:
        service.users().messages().send(userId='me', body=msg).execute()
        print("email successfully sent")
        return 1
    except errors.HttpError as error:
        print("Error in sending email, error: ")
        print(error)
        return 0


def main(to_mail, *args, **kwargs):
    store = file.Storage(STATIC_ROOT + '/accounts/json/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets((STATIC_ROOT + '/accounts/json/credentials.json'), SCOPES)
        creds = tools.run_flow(flow, store)
    service = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    return send_mail(service, to_mail, **kwargs)
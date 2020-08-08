import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import send_mail


def send_email(email_config, email_subject, email_content, recipients_list):
    try:
        # set up the SMTP server
        smtp_server = smtplib.SMTP(host=email_config['host'], port=email_config['port'])
        smtp_server.starttls()
        smtp_server.login(email_config['user-name'], email_config['password'])
        print("Successfully connected to the SMTP server at %s:%s !!"
              % (email_config['host'], email_config['port']))

        # create a multi-part email message
        # email_message = MIMEMultipart()
        # # setup the parameters of the message
        # email_message['From'] = email_config['user-name']
        # email_message['To'] = ", ".join(recipients_list)
        # email_message['Subject'] = email_subject
        # print(email_message['Subject'])
        # # add in the message body
        # email_message.attach(MIMEText(email_content, 'plain'))
        # send the message via the server set up earlier.
        # smtp_server.send_message(email_message)
        # message = """Subject: {}
        #
        # {}""".format(email_subject, email_content)

        message = 'Subject: {}\n\n{}'.format(email_subject, email_content)

        smtp_server.sendmail(email_config['user-name'], recipients_list, message)

        print("Successfully sent the email notifications!!")
        smtp_server.quit()
    except smtplib.SMTPException as e:
        print("Error while sending email notifications: ", str(e))
    except Exception as ex:
        print("Error while sending email notifications: ", str(ex))
        traceback.print_exc()
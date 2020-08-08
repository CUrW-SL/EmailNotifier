import smtplib
import traceback


def send_email(email_config, email_subject, email_content, recipients_list):
    try:
        # set up the SMTP server
        smtp_server = smtplib.SMTP(host=email_config['host'], port=email_config['port'])
        smtp_server.starttls()
        smtp_server.login(email_config['user-name'], email_config['password'])
        print("Successfully connected to the SMTP server at %s:%s !!"
              % (email_config['host'], email_config['port']))

        message = 'Subject: {}\n\n{}'.format(email_subject, email_content)

        smtp_server.sendmail(email_config['user-name'], recipients_list, message)

        print("Successfully sent the email notifications!!")
        smtp_server.quit()
    except smtplib.SMTPException as e:
        print("Error while sending email notifications: ", str(e))
    except Exception as ex:
        print("Error while sending email notifications: ", str(ex))
        traceback.print_exc()
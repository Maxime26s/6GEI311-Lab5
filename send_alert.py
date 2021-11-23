import os
from twilio.rest import Client
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText

def send_email():

    mail = EmailMessage()

    email_text = "It's a test"

    mail['From'] = '6gei311@gmail.com'
    mail['Pass'] = 'M9hA7C6RN8nr'
    mail['To'] = mail['From']
    mail['Subject'] = "TEST"

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(mail['From'], mail['Pass'])

    except:
        print ('Error logging')

    try:
        server.sendmail(mail['From'], mail['To'], email_text)
        print('Email sent')
    except:
        print('Error sending email')
        return
    server.quit()

def send_sms():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="/!\ Alert /!\ Suspicious movement detected",
                        from_='+15812055890',
                        to='+15815609495'
                 )
    print(message.sid)
if __name__ == "__main__":
    # send_email()
    send_sms()
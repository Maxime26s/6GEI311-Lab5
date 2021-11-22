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
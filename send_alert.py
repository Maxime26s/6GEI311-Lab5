import os
from twilio.rest import Client
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_email(destination):

    mail = EmailMessage()

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dt_string1 = now.strftime("%d%m%y_%H%M%S")

    mail = MIMEMultipart()

    email_text = MIMEText("Mouvement detected on the camera at " + dt_string)
    mail.attach(email_text)

    mail["From"] = "6gei311@gmail.com"
    mail["Pass"] = "M9hA7C6RN8nr"
    mail["To"] = destination
    mail["Subject"] = "Alert - Mouvement detected"

    ImgFileName = "IPcam.png"
    with open(ImgFileName, "rb") as f:
        img_data = f.read()

    if img_data is not None:
        image = MIMEImage(img_data, name="IPcam1_" + dt_string1 + ".png")
        mail.attach(image)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(mail["From"], mail["Pass"])

    except:
        print("Error logging")

    try:
        server.sendmail(mail["From"], mail["To"], mail.as_string())
        print("Email sent")
    except:
        print("Error sending email")
        return
    server.quit()
    return


def send_sms(destination):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    account_sid = 'ACb4d7f2ea83b8f378d0f8febf8b410d4e'
    auth_token = 'fa60d3c004f30b77a1f4bf40f394ace1'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="/!\ Alert /!\ Suspicious movement detected. \n "
        "Check your mail. \n\n" + dt_string,
        from_='+15812055890',
        to=destination,
    )
    print(message.sid)


if __name__ == "__main__":
    # send_email()
    send_sms('+15815609495')

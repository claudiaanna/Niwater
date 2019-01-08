import smtplib
import nexmo
import json
import logging

EMAIL = False
SMS = False
BOTH = False

try:
    with open("smsCredentials.json", "r") as data:
        formSMS = json.load(data)
        SMS = True
except FileNotFoundError:
    SMS = False
    logging.info('No SMS credentials file.')

try:
    with open("emailCredentials.json", "r") as data:
        formEmail = json.load(data)
        EMAIL = True
except FileNotFoundError:
    EMAIL = False
    logging.info('No email credentials file.')

if SMS and EMAIL:
    BOTH = True
else:
    BOTH = False

def sendSMS(message):
    phoneNo = formSMS['phoneNumber']
    client = nexmo.Client()
    
    try:
        client.send_message({
        'from': 'Niwater',
        'to': phoneNo,
        'text': message,
        })
        logging.info('SMS was successfuly sent.')
    except Exception as e:
         logging.info('Sending SMS failed. ' + str(e))

def sendEmail(message):
    username = formEmail['username']
    password = formEmail['password']
    sender = formEmail['sender']
    receiver = formEmail['receiver']
    subject = formEmail['subject']
    msg = "From: {}\nTo: {}\nSubject: {}\n\n{}".format(sender, receiver, subject, message)
    server = smtplib.SMTP('smtp.mail.yahoo.com', 587)

    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)
        server.sendmail(sender, receiver, msg)
        server.quit()    
        logging.info('Email was successfuly send.')
    except Exception as e:
        logging.info('Sending email failed. ' + str(e))

def sendNotification(message):
    if BOTH:
        sendEmail(message)
        sendSMS(message)
    elif EMAIL:
        sendEmail(message)
    elif SMS:
        sendSMS(message)

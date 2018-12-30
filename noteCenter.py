import smtplib
import nexmo
import json

"""
SMS
"""
with open("smsCredentials.json", "r") as data:
    form = json.load(data)

phoneNo = form['phoneNumber']
def sendSMS(message):
    client = nexmo.Client()
    client.send_message({
        'from': 'Niwater',
        'to': phoneNo,
        'text': message,
    })

"""
EMAIL
"""
with open("emailCredentials.json", "r") as data:
    form = json.load(data)

username = form['username']
password = form['password']

def sendEmail(sender, receiver, subject, message):
    msg = "From: {}\nTo: {}\nSubject: {}\n\n{}".format(sender, receiver, subject, message)

    try :
        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)
        for i in range(1):
            server.sendmail(sender, receiver, msg)
        server.quit()    
        return 'Email was successfuly send.'
    except :
        return 'Sending email failed.'
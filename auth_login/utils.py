# creates SMTP session
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import choice

from django.template import loader


def send_email(message, reciver):
    emails = ["cusathostel@gmail.com"]
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    email = choice(emails)
    s.login(email, "hostelmanagement@cusat")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Cusat Hostel Allotment'
    msg['From'] = email
    msg['To'] = reciver
    template = loader.get_template('verify_email.html')
    context = {
        'OTP': message
    }
    html = template.render(context)
    part1 = MIMEText(message, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    # message to be sent
    print(message)
    # sending the mail
    s.sendmail(email, reciver, msg.as_string())

    # terminating the session
    s.quit()

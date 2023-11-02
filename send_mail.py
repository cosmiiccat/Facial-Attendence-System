import os
import smtplib
from email.message import EmailMessage


def mail(mail_to,name):
    email_id = 'iayushch@gmail.com' 
    email_pass = 'xzrr fovs hthx gkgn'

    msg = EmailMessage()
    msg['Subject'] = 'Attendance' 
    msg['From'] = email_id
    msg['To'] = mail_to

    msg.set_content('Hi '+name+' ,\nYour attendance have been marked!!\nThankyou')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pass)
        smtp.send_message(msg)

# mail("ayush345kr@gmail.com","Ayush Kumar")
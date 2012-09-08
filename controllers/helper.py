#! /usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config.settings import mail_info

def send_mail(mail_to_list, subject, content):
    from_mail = mail_info['sender'] + (
                '<' + mail_info['sender_address'] + '>')
    txt = MIMEText(content, 'html')
    txt.set_charset('utf-8')
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_mail
    msg['To'] = ';'.join(mail_to_list)
    msg.attach(txt)
    #try:
    s = smtplib.SMTP()
    s.connect(mail_info['host'])
    s.login(mail_info['sender'], mail_info['sender_password'])
    s.sendmail(mail_info['sender_address'], mail_to_list, msg.as_string())
    s.close()
    return True
    #except Exception as e:
        #print(str(e))
        #return False

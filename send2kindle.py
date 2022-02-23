

#	1577594730_f1c357@kindle.cn


#!/usr/bin/env python3
#coding:utf-8

import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

sender = "1577594730@qq.com"
receivers = [sender,'1577594730_f1c357@kindle.cn']

def email(filename):

    msg = MIMEMultipart()
    msg['From'] = formataddr(["Kindle 管理员", sender])
    msg['To'] = formataddr(["kindle", receivers[0]])
    msg['Subject'] = "电子书同步: %s" % filename
    msg.attach(MIMEText(filename, 'plain', 'utf-8'))

    att = MIMEApplication(open(filename, 'rb').read())
    att.add_header(
        'Content-Disposition',
        'attachment',
        filename=Header(filename, "utf-8").encode())

    msg.attach(att)

    try:
        server = smtplib.SMTP("smtp.qq.com")
        #授权码 mjcskqlupgwyfgba
        server.login(sender, "mjcskqlupgwyfgba")
        server.sendmail(sender, receivers, msg.as_string())
        print("*邮件* %s 发送成功!" % filename)
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)


import os,time

if __name__ == '__main__':
    todayFile = "data/cnn_"+time.strftime("%y%m%d", time.localtime())+".txt"
    files = [todayFile]

    for filename in files:
        email(filename)


import smtplib
import uuid

import datetime

import pymongo

GMAIL_USERNAME = 'SKOHuest'
GMAIL_PASSWORD = 'um-its-center'

class GMailPy():
    def __init__(self, username=GMAIL_USERNAME, password=GMAIL_PASSWORD):
        self.username = username
        self.password = password
        self.fromaddr = username
        self.toaddrs = []
        self.subject = ''
        self.message = ''

        self.connection = pymongo.connection.Connection()
        self.db = self.connection.atlitepy

    def add_to_addr(self, toaddr):
        self.toaddrs.append(toaddr)

    def set_subject(self, subject):
        self.subject = subject

    def set_message(self, message):
        self.message = message

    def send_message(self):
        guid = str(uuid.uuid4())
        self.db.mail_log.insert({
            'log':'smtp server started with id: %s' % (guid),'timestamp':datetime.datetime.now()
        })
        smtp = smtplib.SMTP('smtp.gmail.com:587')
        smtp.starttls()
        smtp.login(self.username, self.password)
        for to_addr in self.toaddrs:
            body = """\
            From: %s
            To: %s
            Subject: %s

            %s
            """ % (self.fromaddr, to_addr, self.subject, self.message)
            smtp.sendmail(self.fromaddr, to_addr, body)
            self.db.mail_log.insert({
            'log':'smtp server sent message to %s with id: %s' % (to_addr, guid),'timestamp':datetime.datetime.now()
        })
        smtp.quit()

        self.db.mail_log.insert({
            'log':'smtp server finished with id: %s' % (guid),'timestamp':datetime.datetime.now()
        })


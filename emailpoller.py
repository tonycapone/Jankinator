#!/usr/bin/python

import sys
import imaplib
import email
import time
import json
from bs4 import BeautifulSoup
import retaliation


def getEmail():
    body = ""
    try:
        mail = imaplib.IMAP4('anthonyrhowell.net')
    except:
        return body
    mail.login('retaliation', 'savvis')


    mail.select("inbox") # connect to inbox.

    result, data = mail.search(None, "ALL")

    ids = data[0] # data is a list.
    id_list = ids.split() # ids is a space separated string

    if(len(id_list) > 0):
        latest_email_id = id_list[-1] # get the latest

        result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
        mail.store(latest_email_id, '+FLAGS', '\\Deleted')
        mail.expunge()

        raw_email = data[0][1]

        msg = email.message_from_string(raw_email)

        if msg.is_multipart():
            for payload in msg.get_payload():
                # if payload.is_multipart(): ...
                rawBody = payload.get_payload()
        else:
            rawBody = msg.get_payload()


        body = BeautifulSoup(rawBody).get_text()
        mail.logout()
    return body

def main(args):
    while(True):
        body = getEmail()

        if(body != ""):
            jenkins = json.loads(body)

            coordsFile = open("coords.json")
            coordMap = json.loads(coordsFile.read())
            coordsFile.close()

            culprit = jenkins["reason"].replace("Started by user ", "")

            argStr = "led 1 " + coordMap[culprit] + " fire 1 led 0 reset"

            args = argStr.split()

            args.insert(0, "retaliation.py")
            print "retaliation.py " + argStr
            retaliation.main(args)

        time.sleep(5)

if __name__ == '__main__':
    main(sys.argv)
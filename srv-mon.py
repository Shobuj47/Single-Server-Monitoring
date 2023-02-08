import subprocess
import sys

import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


MAIL_HOST="smtp.example.com"
MAIL_PORT=465
sender_email = "sender_email@example.com"
receiver_email = "receiver1@example.com, receiver2@example.com"
password = "secret password"
HOST="username@host_or_ipaddress"
MSG=''

cmd_zs="systemctl status --no-pager service_name.service | grep 'Active.*.\(running\)'"
cmd_za="systemctl status --no-pager service_name.service | grep 'Active.*.\(running\)'"
cmd_storage="df -H | grep -E '\/dev\/root|\/app|\/db' | awk '{v=($5+00)} v > 80'"

now = datetime.now()


def get_data(_cmd):
        ssh = subprocess.Popen(["ssh", "%s" % HOST, _cmd], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
                return ssh.stderr.readlines()
                print >>sys.stderr, "ERROR: %s" % error
                MSG=MSG + " || " + ssh.stderr.readlines()
        else:
                return result


def send_email(body):
	subject = "Monitoring Server Services Alert"
	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = receiver_email
	message["Subject"] = subject
#	message["Cc"] = cc_email  # Recommended for mass emails
	# Add body to email
	message.attach(MIMEText(body, "plain"))

	text = message.as_string()

	# Log in to server using secure context and send email
	context = ssl.create_default_context()
	server = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT, context )
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, text)
	server.quit()



if get_data(cmd_zs) == []:
	MSG = MSG + ' \n * Service Error : Service Name'
if get_data(cmd_za) == []:
	MSG = MSG + ' \n * Service Error : Service Name'

storage_util=get_data(cmd_storage)

if storage_util != []:
    MSG = MSG + ' \n * Failed : Storage Utilization is high : ' + str(storage_util)

if MSG != '':
	print "--------------------------"
	print str(now) + ' > ' + MSG
	print "--------------------------"
        body = "\nDear Concern,\n\n Monitoring Server has some critical allert. Alert list is given blow:\n" + MSG + "\n\n" +  str(now)
	send_email(body)
	

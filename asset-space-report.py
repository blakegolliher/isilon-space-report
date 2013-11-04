#!/usr/bin/python
##
#
# A simple script to collect Used and Free space on
# a collection of isilon clusters and email out the
# data as a weekly report.
#
# Blake Golliher - blakegolliher@gmail.com
#
##

import sys, os
import netsnmp
import smtplib
from email.mime.text import MIMEText
import datetime

# Add more clusters here.
primcluster = (
  "isi01",
  "isi02")
drcluster = (
  "drisi01",
  "drisi02")

communitystring = 'isisnmpstring'
date = datetime.datetime.now().strftime( "%m/%d/%Y - %H:%M" )

def sizeof_fmt(num):
    """ Convert a number of bytes to a human readable size """
    for x in ["B", 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def getnfs(target):
  session = netsnmp.Session(DestHost=target, Version=2, Community=communitystring)
	uspacevar = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.12124.1.3.2.0'))
	aspacevar = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.12124.1.3.3.0'))
	uspace  = session.get(uspacevar)
	aspace  = session.get(aspacevar)
  used = ''.join(c for c in uspace if c not in '()')
 	avail = ''.join(c for c in aspace if c not in '()')
## you can print this out if you want the output on the console
## print "\t\t%s - has %s used and %s available." % (target, sizeof_fmt(int(used)), sizeof_fmt(int(avail)))
	return "\t\t%s - has %s used and %s available." % (target, sizeof_fmt(int(used)), sizeof_fmt(int(avail)))

## cleans up from the last run
if os.path.exists('./data'):
    os.remove('./data')

data=open('./data', 'w+')
data.write("Primary Isilon Clusters :: Space Report\n")

for clustername in primcluster:
	data.write("\t%s\n" % getnfs(clustername))

data.write("\nDR Isilon Clusters :: Space Report\n")

for clustername in drcluster:
	data.write("\t%s\n" % getnfs(clustername))

data.close()

data = open('./data', 'rb')
msg = MIMEText(data.read())
data.close()

FROM = 'snakemail@somewhere.com'
TO = ['blakegolliher@gmail.com']

msg['Subject'] = 'Isilon Cluster Usage Report : %s' % dateort'
msg['To'] = ", ".join(TO)

s = smtplib.SMTP('localhost')
s.sendmail(FROM, TO, msg.as_string())
s.quit()

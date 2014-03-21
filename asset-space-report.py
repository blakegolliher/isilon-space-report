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
        tspacevar = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.12124.1.3.1.0'))
        uspace  = session.get(uspacevar)
        aspace  = session.get(aspacevar)
        tspace  = session.get(tspacevar)
        pspace = float(aspace[0]) / float(tspace[0]) * 100
        print "\t\t%s : used = %s : availible space = %s : free = %.2f %% " % (target, sizeof_fmt(int(uspace[0])), sizeof_fmt(int(aspace[0])), pspace)
        return "\t\t%s : used = %s : availible space = %s : free = %.2f %% " % (target, sizeof_fmt(int(uspace[0])), sizeof_fmt(int(aspace[0])), pspace)
        
## cleans up from the last run
if os.path.exists('./data'):
    os.remove('./data')

hostami = os.getenv('HOSTNAME')
whereami = os.getcwd()
whoami = os.path.basename(__file__)

f1=open('./data', 'w+')
f1.write("Sent from : %s:%s/%s \n\n" % (hostami,whereami,whoami))

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

msg['Subject'] = 'Isilon Cluster Usage Report : %s' % date
msg['To'] = ", ".join(TO)

s = smtplib.SMTP('localhost')
s.sendmail(FROM, TO, msg.as_string())
s.quit()

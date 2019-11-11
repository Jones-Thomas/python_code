import wmi
from socket import *
import psutil
import datetime
import time

ip = ["10.2.1.154","10.2.1.155","10.2.1.156"]
username = "ge-dev\jthomas-admin"
password = "7qAaNHewf8AP8kK#$@"
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

for h in ip:
  try:
    #print ("Establishing connection to %s" %h)
    connection = wmi.WMI(h, user=  username, password=password)
    #print ("Connection established")
    for i in connection.Win32_service():
       if i.Caption == 'globaledit Worker':
        print (st ,"-", h , i.SystemName, i.Caption,":", i.State,":", i.Status,":" ,i.ProcessId)
        f= open('Stg-worker-check.txt', 'a+')
        print (st , i , file=f)
  except wmi.x_wmi:
    print ("Your Username and Password of "+getfqdn(ip)+" are wrong.")

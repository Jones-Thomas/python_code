import wmi
from socket import *
import psutil
from decimal import Decimal
from psutil._common import bytes2human

ip = ["10.2.1.1x4","10.2.1.x55","10.2.1.xx6"]
username = "domain\user"
password = "7qAaNHewf8AP8kK#$@"
mem = psutil.virtual_memory()
mem_total = bytes2human(mem.total)
mem_avail = bytes2human(mem.available)
mem_used = bytes2human(mem.used)
mem_free = bytes2human(mem.free)

for h in ip:
  try:
    #print ("Establishing connection to %s" %h)
    connection = wmi.WMI(h, user=  username, password=password)
    #print ("Connection established")
    for i in connection.Win32_service():
       if i.Caption == 'globaledit Worker':
        print (h, i.SystemName, i.Caption, i.State, i.Status, mem_total , mem_avail, mem_used, mem_free)
        #f= open('Stg-worker-check.txt', 'a+')
        #print (i , file=f)
  except wmi.x_wmi:
    print ("Your Username and Password of "+getfqdn(ip)+" are wrong.")

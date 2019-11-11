import wmi
from socket import *
import psutil
from decimal import Decimal
from psutil._common import bytes2human
import datetime
import time

ip = ["10.2.1.154","10.2.1.155","10.2.1.156"]
username = "ge-dev\jthomas-admin"
password = "7qAaNHewf8AP8kK#$@"
mem = psutil.virtual_memory()
mem_total = bytes2human(mem.total)
mem_avail = bytes2human(mem.available)
mem_used = bytes2human(mem.used)
mem_free = bytes2human(mem.free)
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

for h in ip:
  try:
    #print ("Establishing connection to %s" %h)
    connection = wmi.WMI(h, user=  username, password=password)
    #print ("Connection established")
    for i in connection.Win32_service():
       if i.Caption == 'globaledit Worker':
        Final_out = print (st ,"-", h, i.SystemName, i.Caption,":", i.State,"->", i.Status,":", "Mem_Total: " + mem_total , "Mem_Avail: " + mem_avail, "Mem_Used: " + mem_used, "Mem_Free: " + mem_free)
        f= open('Stg-worker-check.txt', 'a+')
        print (final_out , file=f)
  except wmi.x_wmi:
    print ("Your Username and Password of "+getfqdn(ip)+" are wrong.")

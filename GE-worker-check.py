import wmi
from socket import *
import psutil
from decimal import Decimal
from psutil._common import bytes2human
import datetime
import time

ip = ["10.2.1.1*4","10.2.1.*55","10.2.1.1*6"]
username = "Domain\user"
password = "7qAaNHewf8AP8kK#$@"
mem = psutil.virtual_memory()
mem_total = bytes2human(mem.total)
mem_avail = bytes2human(mem.available)
mem_used = bytes2human(mem.used)
mem_free = bytes2human(mem.free)
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
final_out=""

for h in ip:
  try:
    #print ("Establishing connection to %s" %h)
    connection = wmi.WMI(h, user=  username, password=password)
    #print ("Connection established")
    for i in connection.Win32_service():
       if i.Caption == 'globaledit Worker':
          print (st ,"-", h,"-", i.SystemName,"-", i.Caption,":", i.State,"~", i.Status,"-->", " Mem_Total: " + mem_total , " Mem_Avail: " + mem_avail, " Mem_Used: " + mem_used, "Mem_Free: " + mem_free)
          final_out = (st ,"-", h,"-", i.SystemName,"-", i.Caption,":", i.State,"~", i.Status,"-->", " Mem_Total: " + mem_total , " Mem_Avail: " + mem_avail, " Mem_Used: " + mem_used, "Mem_Free: " + mem_free)
    with open('Stg-worker-check.txt', 'a+') as f:
         print (final_out , file=f)
  except wmi.x_wmi:
    print ("Your Username and Password of "+getfqdn(ip)+" are wrong.")

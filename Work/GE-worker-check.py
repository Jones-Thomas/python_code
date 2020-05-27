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
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


for h in ip:
  try:
    connection = wmi.WMI(h, user=  username, password=password)
    for i in connection.Win32_service():  
      if i.Caption == 'globaledit Worker':
        service_check = (st , h, i.SystemName, i.Caption, i.State, i.Status)
        print (st ,"-", h,"-", i.SystemName,"-", i.Caption,":", i.State,"~", i.Status)
    for vm in connection.Win32_ComputerSystem():
      vmm=int(vm.TotalPhysicalMemory)
      Memory_check = ("Total_Memory", bytes2human(vmm))
      print ("Total_Memory", bytes2human(vmm))

    final_out = (service_check , Memory_check)
    with open('Prod-3-worker-check.txt', 'a+') as f:
        print (final_out , file=f)
  except wmi.x_wmi:
    print ("Your Username and Password of "+ getfqdn(ip)+" are wrong.")

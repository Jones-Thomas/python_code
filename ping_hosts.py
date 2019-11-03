#Import the libraries
import os
import re
import sys


hostname = "www.google.com"
print("Staring to Ping the host" )
ping_host = os.system("ping -c 5 "+ hostname + " > /dev/null 2>&1")
print("Ping got completed !")

if ping_host == 0:
   
      outputs = (hostname , "The server is up!")

else:
   
      outputs = (hostname, "The server is down")
      
print(outputs)


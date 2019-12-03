from datetime import datetime
from elasticsearch import Elasticsearch
import json
import requests
import time

es = Elasticsearch([{'host':'localhost', 'port':'9200'}]) 
res = es.cluster.health()


while (res["status"] != "green") :
    res = es.cluster.health()
    print ("Status is Still: ", res["status"])
    print ("Total Unassigned shards: ", res["unassigned_shards"])
    time.sleep(60)
print (res["status"])

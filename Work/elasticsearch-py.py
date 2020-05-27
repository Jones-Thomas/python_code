from datetime import datetime
from elasticsearch import Elasticsearch
import time
import json
start_time = time.time()
es = Elasticsearch([{'host': 'geall-lxkibana01.ics.com', 'port': '9200'}])
result_item = (es.get(index='logstash-globaledit_api-2019.11.19',
                      id='AW6FtLbsQax-V1xMi_m0',
                      doc_type='globaledit'))


k = result_item.items()
if result_item['_source']['Level'] == 'ERROR':
    res = ("Time", result_item['_source']['Date'],
           "Level", result_item['_source']['Level'],
           "Data", result_item['_source']['Message']['Data'])
    print(res)

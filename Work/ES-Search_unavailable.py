from datetime import datetime
from elasticsearch import Elasticsearch
import time
import json
import requests


start_time = time.time()
es = Elasticsearch([{'host': 'geall-lxkibana01.ics.com', 'port': '9200'}])

HEADSERS = {'Content-Type': 'application/json'}
uri = "http://geall-lxkibana01.ics.com:9200/logstash-*/_search"

# result_item = es.search(index='logstash-globaledit_api-*',
#                         body=docss, scroll='1m')

querys = json.dumps({
    "size": 500,
    "sort": [
        {
            "@timestamp": {
                "order": "desc",
                "unmapped_type": "boolean"
            }
        }
    ],
    "highlight": {
        "pre_tags": [
            "@kibana-highlighted-field@"
        ],
        "post_tags": [
            "@/kibana-highlighted-field@"
        ],
        "fields": {
            "*": {}
        },
        "fragment_size": 2147483647
    },
    "query": {
        "filtered": {
            "query": {
                "query_string": {
                    "query": "Message.Data: \"SearchUnavailable*\"",
                    "analyze_wildcard": True
                }
            },
            "filter": {
                "bool": {
                    "must": [
                      {
                          "range": {
                              "@timestamp": {
                                  "gte": 1573975403772,
                                  "lte": 1574580203772
                              }
                          }
                      }
                    ],
                    "must_not": []
                }
            }
        }
    },
    "aggs": {
        "2": {
            "date_histogram": {
                "field": "@timestamp",
                "interval": "3h",
                "pre_zone": "+05:30",
                "pre_zone_adjust_large_interval": True,
                "min_doc_count": 0,
                "extended_bounds": {
                    "min": 1573975403772,
                    "max": 1574580203772
                }
            }
        }
    },
    "fields": [
        "*",
        "_source"
    ],
    "script_fields": {},
    "fielddata_fields": [
        "@timestamp",
        "Message.SearchContextLogData`1.ResponseBody.AddedOn",
        "Message.SearchContextLogData`1.ResponseBody.StarRatingDateTime",
        "Message.SearchContextLogData`1.ResponseBody.ApprovedDateTime",
        "Message.SearchContextLogData`1.ResponseBody.SelectDateTime",
        "Message.SearchContextLogData`1.ResponseBody.AltDateTime",
        "Message.SearchContextLogData`1.ResponseBody.KilledDateTime",
        "Message.SearchContextLogData`1.ResponseBody.CreatedOn",
        "Message.SearchContextLogData`1.ResponseBody.ModifiedOn",
        "logdate",
        "Message.DeviceNotification.EnqueuedTimestamp",
        "Message.ApiVersion",
        "Message.SearchContextLogData`1.ResponseBody.RightsRestriction",
        "Message.@timestamp"
    ]
})
l = []
r = (requests.post(uri, headers=HEADSERS, data=querys).json())
res = dict(r)
total_hit = res['hits']['total']
lenght_hit = len(res['hits']['hits'])
print("Total_Hits: ", total_hit)
for i in range(lenght_hit):
    date_time = res['hits']['hits'][i]['_source']['Date']
    level = res['hits']['hits'][i]['_source']['Level']
    message_data = res['hits']['hits'][i]['_source']['Message']['Data']
    final_out = (date_time, level, message_data)
    print(final_out)

import sys
import pyodbc as mysql
import pandas as pd
import numpy as np
from slacker import Slacker 
import json
import time
import logging


slack_token = Slacker("xoxb-2328284242-1132712822385-dqWd8mgNI1pAsdb3aRcKW5hl")
db = mysql.connect(SERVER='PRD-DB-02.ics.com', Database='GE', DRIVER='{SQL Server}', UID='sa', PWD='SQL h@$ N0 =',Trusted_Connection='no')
cursor = db.cursor()

sqlquery1= """
DECLARE @today date = GETDATE();
select d.DownloadedBy as Username,d.Filename,d.FileByteCount,d.Time as CreatedOn from vw_DownloadedFiles d
inner join Account a on a.AccountID=d.AccountID
where d.AccountID=3389 and d.Time >= @today order by d.Time asc;
"""
df = pd.read_sql(sqlquery1,db)



df_new = df.groupby(['Username'], as_index=False).agg({'FileByteCount': 'sum'})
df_new['FileByteCount']=(df_new['FileByteCount'] / (1024*1024*1024)).round(2)
df_new=(df_new[df_new['FileByteCount'].values >= 10])
df_new= df_new.reset_index(drop=True)
username=df_new['Username'].str.strip().to_list()
print(username)


df_new1 = df[df['Username'].isin(df_new['Username'])]
df_new1= df_new1.reset_index(drop=True)
print(df_new1)

    
# mergedf= pd.merge(df_new,df_new1, on="Username")
# print(mergedf)
#df['Filename'], df['FileByteCount'], df['CreatedOn']

    
for index, row in df_new.iterrows():
    print(index, row['Username'],row['FileByteCount'])
    sample_list=[
	{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "`ALERT:` *Amazon Download file size greater than 10_GB*"
		}
	},
	{
		"type": "section",
		"fields": [
            {
				"type": "mrkdwn",
				"text": "*UserName:* "+ str(row['Username'])
			},
			{
				"type": "mrkdwn",
				"text": "*Total_Download_SizeInGB:* "+ str(row['FileByteCount'])
			}			
		]
	}
    ]
    slack_token.chat.post_message('#z-download-report', blocks=json.dumps(sample_list));


#df.to_csv('./dowload_report.csv', index=False)
logging.basicConfig(filename='./app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
print("Message sent!")

import sys
import pyodbc as mysql
import pandas as pd
import numpy as np
from slacker import Slacker 
import json
import time
import logging


slack_token = Slacker("xoxb-2328284242-1132712822385-OCe1fGGiJbWQ0G89fdjIuIPP")
db = mysql.connect(SERVER='PRD-DB-02.ics.com', Database='GE', DRIVER='{SQL Server}', UID='sa', PWD='SQL h@$ N0 =',Trusted_Connection='no')
cursor = db.cursor()

sqlquery1= """
DECLARE @today date = GETDATE();
select d.DownloadedBy as Username,d.Filename,d.FileByteCount,d.Time as CreatedOn from vw_DownloadedFiles d
inner join Account a on a.AccountID=d.AccountID
where d.AccountID=3389 and d.Time >= DATEADD(DAY, -5, @today) and d.Time <  @today order by d.Time asc;
"""
df = pd.read_sql(sqlquery1,db)

# for index, row in df.iterrows():
#     print(index, row['UserID'],row['FullName'],row['CreatedOn'],row['Name'],row['SizeInGB'])
#     sample_list=[
# 	{
# 		"type": "section",
# 		"text": {
# 			"type": "mrkdwn",
# 			"text": "*Amazon Download file size greater than 10_GB*"
# 		}
# 	},
# 	{
# 		"type": "section",
# 		"fields": [
#             {
# 				"type": "mrkdwn",
# 				"text": "*User-ID:*\n"+ str(row['UserID'])
# 			},
# 			{
# 				"type": "mrkdwn",
# 				"text": "*User-FullName:*\n"+ str(row['FullName'])
# 			},
# 			{
# 				"type": "mrkdwn",
# 				"text": "*CreatedOn:*\n"+ str(row['CreatedOn'])
# 			},
# 			{
# 				"type": "mrkdwn",
# 				"text": "*DownloadName*\n"+ str(row['Name'])
# 			},
# 			{
# 				"type": "mrkdwn",
# 				"text": "*SizeInGB:*\n"+ str(row['SizeInGB'])
# 			}			
# 		]
# 	}
#     ]
#     #slack_token.chat.post_message('#z-download-report', blocks=json.dumps(sample_list));


# #df.to_csv('./dowload_report.csv', index=False)
# logging.basicConfig(filename='./app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
# print("Message sent!")

#print(df)


df_new = df.groupby(['Username'], as_index=False).agg({'FileByteCount': 'sum'})
df_new['FileByteCount']=(df_new['FileByteCount'] / (1024*1024*1024)).round(2)
df_new=(df_new[df_new['FileByteCount'].values >= 1])
df_new= df_new.reset_index(drop=True)
username=df_new['Username'].str.strip().to_list()
print(username)


df_new1 = df[df['Username'].isin(df_new['Username'])]
df_new1= df_new1.reset_index(drop=True)
print(df_new1)

    
# mergedf= pd.merge(df_new,df_new1, on="Username")
# print(mergedf)
#df['Filename'], df['FileByteCount'], df['CreatedOn']
x=0
for x in df_new1:
    df_new1[df_new1['Username'] == username[x]]
    

    

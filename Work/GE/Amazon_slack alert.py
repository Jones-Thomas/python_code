import sys, json, time, logging
import pyodbc as mysql
import pandas as pd
import numpy as np
from slacker import Slacker 



slack_token = Slacker("xoxb-2328284242-1132712822385-9gKknBlgxJcvWUT84xea67qW")
db = mysql.connect(SERVER={HOST}, Database={DATABASE}, DRIVER='{SQL Server}', UID='sa', PWD={PASSWORD},Trusted_Connection='no')
cursor = db.cursor()

sqlquery1= """
SET NOCOUNT ON
declare @AccID int =3389;
Declare @NoOfDays int = 2;
with CTE as(
select distinct vd.DownloadID,vd.DownloadedBy as UserName,vd.Filename,vd.FileByteCount,vd.Time as CreatedOn,[dbo].[udf_GetFolderPath](jf.JobFolderID) as[FolderPath] From vw_DownloadedFiles vd 
inner join Download d on vd.DownloadID=d.DownloadID
inner join FilePackage fp on d.FilePackageID=fp.FilePackageID
inner join FilePackageAssets fpa on fp.FilePackageID=fpa.FilePackageID
inner join Asset a on fpa.AssetID=a.AssetID
left join JobFolder jf on a.JobFolderID=jf.JobFolderID
where vd.AccountID= @AccID AND vd.Time >= DATEADD(day,- @NoOfDays, CONVERT(varchar,Getdate(),1))  AND vd.DownloadType IN ('Assets')
union
select distinct vd.DownloadID,vd.DownloadedBy as UserName,vd.Filename,vd.FileByteCount,vd.Time as CreatedOn,[dbo].[udf_GetFolderPath](jf.JobFolderID) as[FolderPath]
From vw_DownloadedFiles vd 
inner join Asset a on vd.AssetID=a.AssetID
left join JobFolder jf on a.JobFolderID=jf.JobFolderID
where vd.AccountID=@AccID AND vd.Time >= DATEADD(day,- @NoOfDays, CONVERT(varchar,Getdate(),1))  and vd.AssetID is NOT NULL
union
 select distinct vd.DownloadID,vd.DownloadedBy as UserName,vd.Filename,vd.FileByteCount,vd.Time as CreatedOn,[dbo].[udf_GetFolderPath](jf.JobFolderID) as[FolderPath] 
 from vw_DownloadedFiles vd
inner join Download d on d.DownloadID=vd.DownloadID
inner join FilePackage fp on fp.FilePackageID=d.FilePackageID
inner join LightBox lf on fp.LightboxID=lf.LightboxID
inner join LightboxAsset lba on lba.LightboxID=lf.LightboxID
inner join Asset a on a.AssetID=lba.AssetID
inner join JobFolder jf on jf.JobFolderID=a.JobFolderID
 where vd.DownloadType IN ('Lightbox (zip)','Lightbox (Aspera)','ContactSheet') AND vd.AccountID=@AccID
And vd.Time >= DATEADD(day,-@NoOfDays, CONVERT(varchar,getdate(),1))
)

select DownloadID, UserName, FileName, FileByteCount, CreatedOn, max(FolderPath) as FolderPath,
SUBSTRING(max(FolderPath), 1 ,
                      case when  CHARINDEX('\\', max(FolderPath) ) = 0 then LEN(max(FolderPath)) 
                     else CHARINDEX('\\', max(FolderPath)) -1 end) as ShowName
from CTE
group by DownloadID, UserName, FileName, FileByteCount, CreatedOn
"""
df = pd.read_sql(sqlquery1,db)

df_new = df.groupby(['UserName'], as_index=False).agg({'FileByteCount': 'sum'})
df_new['FileByteCount']=(df_new['FileByteCount'] / (1024*1024*1024)).round(2)
df_new=(df_new[df_new['FileByteCount'].values >= 10])
df_new= df_new.reset_index(drop=True)
username=df_new['UserName'].str.strip().to_list()
print(username)


df_new1 = df[df['UserName'].isin(df_new['UserName'])]
df_new1= df_new1.reset_index(drop=True)
print(df_new1)

print() 


for index, row in df_new.iterrows():
    print(index, row['UserName'],row['FileByteCount'])
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
				"text": "*UserName:* "+ str(row['UserName'])
			},
			{
				"type": "mrkdwn",
				"text": "*Total_Download_SizeInGB:* "+ str(row['FileByteCount'])
			}			
		]
	}
    ]
    #slack_token.chat.post_message('G0141PSFBL4', blocks=json.dumps(sample_list));
    slack_token.chat.post_message('#z-download-report', blocks=json.dumps(sample_list));


df.to_csv('./dowload_report.csv', index=False, mode='a')
logging.basicConfig(filename='./app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
print("Message sent!")

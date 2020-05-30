import pandas as pd


df=pd.read_csv("D:\\Jones\\Python\\VS_Code_python\\Amazon_DotLG\\Amazon_dotLG.csv") 
print(df)

df = df.groupby(['Filename']).size().reset_index(name='count')
print(df)

df=df[~df['Filename'].str.contains("_lg")]
print(df)
df['Filename']=df['Filename'].str.replace(".lg.jpg", ".jpg")
df=df['Filename']
#df.to_excel('./Amazon_jpg_count.xlsx',sheet_name= 'AssetWithJPG', index=False)
df.to_csv('./Amazon_jpg_count.csv',index=False, header=True)v

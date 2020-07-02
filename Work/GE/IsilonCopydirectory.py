import shutil , os, sys
import pandas as pd

# shutil.copy2('U:\\ge_storage\\ge_objects\\0000\\2C4F\\46462615\\fs_js_170808_cameron_white_0184.jpg', 'C:\\Users\\jthomas-admin\\Downloads\\HookStudio\\test\\')

df = pd.read_csv('C:\\Users\\jthomas-admin\\Documents\\Jones\\bin\\python\\HookStudioCopy\\HookStudio_MissingAsset.csv')

file_path = ('U:\\ge_storage\\ge_objects\\')
Dest_path = ('C:\\Users\\jthomas-admin\\Downloads\\HookStudio\\')
print(df)

for index, row in df.iterrows():
    if not os.path.exists(Dest_path + row['FolderPath'] ):
        os.makedirs(Dest_path + row['FolderPath'] )
    shutil.copy2(file_path + row['StorageFolderPath']+'\\' + row['Filename'], Dest_path + row['FolderPath'] + '\\', follow_symlinks=True)
    print(row['AssetID'], row['Filename'] , "Copied!" )


print("END")

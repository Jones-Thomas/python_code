import pandas as pd

chunk_size = 50
batch_no = 1

for chunk in pd.read_csv('D:\\Jones\\Python\\VS_Code_python\\Chunk_CSV\\Asset_details_test_S3.csv', chunksize=chunk_size):
    chunk.to_csv('Asset_details_test_S3' + str(batch_no) + '.csv', index=False)
    batch_no +=1
    
print("Done")

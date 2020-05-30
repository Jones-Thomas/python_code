import os
import pandas as pd


#Enter the path to find the list in directory
path1=input("Enter the Path: ")

for filename in os.listdir(path1):
    print(filename)
    
print("Done")

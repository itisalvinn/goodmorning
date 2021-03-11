import os
from tools import industryCount, groupTickers, fileFilter, mergeFiles

"""
To analyze the number of 'high gain' industries over a period (n days) 
TODO: look into yfinance to grab tickers in question 
"""

# check if there are excel files to analyze
subDir = 'gains'
files = os.listdir(os.chdir(subDir))
n = int(input("Period to analyze (in days) : "))
print(f"Analyzing previous {n} days of data ...")
industrySet = set()

if files:
    # do some analysis
    print(f"Counting high gain industries ...")
    
    dataframe = mergeFiles(fileFilter(files, n))
    industryCount(dataframe)
    groupTickers(dataframe)
    
else:
    print("no files to analyze")

print("Done!!! :) ")

# filter relevant files
# concat sheets together by common headers (?)
# given industry headers we add it to a set OR add industry header + count to a map

# goal :
# 1) data set with industry header + respective freq count
# 2) data set with industry header + respective tickers



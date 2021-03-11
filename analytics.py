import os
from tools import industryCount, groupTickers, fileFilter, mergeFiles, writeToExcelIndustry, writeToExcelTickers

"""
To analyze the number of 'high gain' industries over a period (n days inclusive) 
TODO: look into yfinance to grab tickers in question 
"""

# check if there are excel files to analyze
subDir = 'gains'
files = os.listdir(os.chdir(subDir))
n = int(input("Period to analyze (in days) : "))
print(f"Analyzing previous {n} days of data ...")

if files:
    # do some analysis
    print(f"Counting high gain industries ...")
    
    dataframe = mergeFiles(fileFilter(files, n))
    indData = industryCount(dataframe)
    tickerData = groupTickers(dataframe)
    writeToExcelIndustry(indData, n)
    # writeToExcelTickers(tickerData, n)
    
else:
    print("Error: no files to analyze")

print("Done!!! :) ")


# goal :
# 1) data set with industry header + respective freq count
# 2) data set with industry header + respective tickers



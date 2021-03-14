import os
import analyticsUtil as au

"""
To analyze the number of 'high gain' industries over a period (n days inclusive) 
TODO: look into yfinance to grab tickers in question 
"""

subDir = 'gains'
files = os.listdir(os.chdir(subDir))
n = int(input("Period to analyze (in days) : "))
print(f"Analyzing previous {n} days of data ...")
filteredFiles = au.fileFilter(files, n)

if filteredFiles:
    # do some analysis
    print(f"Counting high gain industries ...")
    
    dataframe = au.mergeFiles(filteredFiles)
    os.chdir('..')
    indData = au.industryCount(dataframe)
    tickerData = au.groupTickers(dataframe)
    au.writeToExcelIndustry(indData, n)
    au.writeToExcelTickers(tickerData, n)
    
else:
    print("Error: no files to analyze")

print("Done!!! :) ")

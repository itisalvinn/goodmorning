import os
import analyticsUtil as au
import yfinance as yf

"""
To analyze the number of 'high gain' industries over a period (n days inclusive) 
TODO: look into yfinance to grab tickers in question 
"""

subDir = 'gains'
files = os.listdir(os.chdir(subDir))
n = int(input("Period to analyze (in days) : "))
print(f"Analyzing previous {n} days (inclusive) of data ...\n")
filteredFiles = au.fileFilter(files, n)

if filteredFiles:
    dataframe = au.mergeFiles(filteredFiles)
    # need to write to excel from parent directory
    os.chdir('..')
    indData = au.industryCount(dataframe)
    tickerData = au.groupTickers(dataframe)
    au.writeToExcelIndustry(indData, n)
    au.writeToExcelTickers(tickerData, n)
    
else:
    print("Error: no files to analyze")

print("\nDone!!! :) ")

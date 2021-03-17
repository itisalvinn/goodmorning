import os
import analyticsUtil as au

"""
To analyze the number of 'high gain' industries over a period (n days inclusive) 
"""

subDir = 'gains'
files = os.listdir(os.chdir(subDir))
n = int(input("Period to analyze (in days) : "))
print(f"Analyzing previous {n} days (inclusive) of data ...\n")
# filteredFiles = au.fileFilter(files, n)
filteredFiles = []

try:
    print(f"Found {len(filteredFiles)} file(s)\n")
    dataframe = au.mergeFiles(filteredFiles)
    # need to write to excel from parent directory
    os.chdir('..')
    indData = au.industryCount(dataframe)
    tkrData = au.groupTickers(dataframe)
    au.writeToExcelIndustry(indData, n)
    au.writeToExcelTickers(tkrData, n)

except ValueError as err:
    print(f"Yikes. Found 0 files to analyze")
    print(err)

finally:
    print("\nDone!!! :) ")

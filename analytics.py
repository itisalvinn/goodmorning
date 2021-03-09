import os
from tools import analytics, fileFilter

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
    for f in fileFilter(files, n):
        print(f)
        # analytics(f, industrySet)
else:
    print("no files to analyze")

print("Done!!! :) ")

# method takes in n days
# backtrack today - n and retrieve all relevant data
    # if the weekday is > 4 (or if file contains CLOSED) we skip it
# for each file, we get a tuple of their industry and increment a count for each unique one (use set)


import xlsxwriter
import pandas as pd
from datetime import date, datetime, timedelta
from collections import Counter

def reminder():
    marketHours = "NASDAQ market hours : Mon-Fri b/w 9:30 am - 4 pm EST"
    print(f"{marketHours}")

def getColWidth(tblHeaders):
    """ 
    method to get length of each column header
    
    :param tblHeaders: 6 columns - ticker, change, company, industry, country, marketCap
    :return: colWidths array containing length of each default col header  
    """

    colWidths = []

    # default 2 units wider than length of original header
    for i in range(len(tblHeaders)):
        colWidths.append(len(tblHeaders[i]) + 2)

    return colWidths

def writeToExcel(data, tblHeaders, colWidths) -> None:
    """
    method to write scraped data into an excel file 
    
    :param data: array of tuples containing stock data scraped from Finviz
    :param tblHeaders: array of headers for excel table
    :param colWidths: array of width lengths 
    :return: none
    """

    today = date.today()
    # monday = 0 ... sunday = 6 TODO: update to use isoweekday() as it is more intuitive
    weekday = today.weekday()

    if weekday > 4:
        backtrack = date.today().weekday() - 4
        friday = today - timedelta(backtrack)
        print("Market is closed")
        fileName = "CLOSED-" + str(today) + '.xlsx'

    else:
        # fileName = str(weekday) + "-" + str(today) + '.xlsx'
        fileName = str(today) + '.xlsx'

    path = 'gains/' + fileName

    # worksheet set up
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    red = workbook.add_format({'font_color': 'red'})

    worksheet.write('A1', tblHeaders[0], bold)
    worksheet.write('B1', tblHeaders[1], bold)
    worksheet.write('C1', tblHeaders[2], bold)
    worksheet.write('D1', tblHeaders[3], bold)
    worksheet.write('E1', tblHeaders[4], bold)
    worksheet.write('F1', tblHeaders[5], bold)

    row = 1
    col = 0
    
    for ticker, change, company, industry, country, marketCap in (data):
        worksheet.write_string(row, col, ticker)
        # negative change highlighted in red
        if float(change.strip('%')) > 0:
            worksheet.write_string(row, col+1, change)
        else:
            worksheet.write_string(row, col+1, change, red)
        worksheet.write_string(row, col+2, industry)
        worksheet.write_string(row, col+3, company)
        worksheet.write_string(row, col+4, country)
        worksheet.write_string(row, col+5, marketCap)

        row += 1
    
    for i in range(len(colWidths)):
        worksheet.set_column(i, i, colWidths[i])

    workbook.close()
    
    print(f"File created in {path}")

def industryCount(dataframe):
    """
    method to grab industry name and a count of how many are in each file

    :param dataframe: dataframe holding a collection of [ticker, industry]
    :param industrySet:
    :return: dictionary containing {'industryName' : count}
    """
    industryDict = {}

    for val in dataframe.values:
        industryDict[val[1]] = industryDict.get(val[1], 0) + 1

    return industryDict

def groupTickers(dataframe):
    """
    method to group tickers by industry

    :param dataframe: dataframe holding a collection of [ticker, industry]
    :return: dictionary containing {'industryName' : 'tickers'}
    """
    tickerDict = {}
    tickerSet = set()

    # get unique tickers for each industry
    for val in dataframe.values:
        if val[1] in tickerDict and val[0] not in tickerSet:
            tickerDict[val[1]].append(val[0])
        else:
            tickerDict[val[1]] = [val[0]]
            tickerSet.add(val[0])
    
    return tickerDict

def fileFilter(files, days):
    """
    filter files up to n days

    :param files: array of excel files retrieved from /gains directory
    :param days: number of previous days to filter for
    :return: filtered array with files generated within the specified time frame
    """
    filteredFiles = []
    timeDiff = date.today() - timedelta(days)

    for f in files:
        if "CLOSED" in f:
            continue

        # grab date portion of file to compare
        fileTime = datetime.strptime(f[:len(f)-5], "%Y-%m-%d").date()

        if fileTime >= timeDiff:
            filteredFiles.append(f)

    return filteredFiles

def mergeFiles(files):
    """
    Merges each file from files array into a DataFrame based on Ticker (col A) and Industry (col C) headers

    :param files: an array of (filtered) excel files
    :return: panda DataFrame of the concatenated files [['ticker', 'industry'], ['ticker', 'industry'], ...]
    """
    
    # read ticker and industry columns into an array of dataframes
    frames = [pd.read_excel(f, index_col=None, engine='openpyxl', usecols="A,C") for f in files]
    combinedFiles = pd.concat(frames)
    return combinedFiles
    
import xlsxwriter
import pandas as pd
from datetime import date, datetime, timedelta

# TODO: consider removing decorator(?)
def industryDec(iDec):
    def indWrapper(dataframe):
        print(f"Counting high gain industries ...")
        return iDec(dataframe)
    return indWrapper

def tickerDec(tDec):
    def tickerWrapper(dataframe):
        print(f"Grouping tickers ...")
        return tDec(dataframe)
    return tickerWrapper

@industryDec
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

@tickerDec
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
    note: method assumes all files in directory are of format 'some-date-time.xlsx'

    :param files: array of excel files retrieved from /gains directory
    :param days: number of previous days to filter for (inclusive)
    :return: filtered array with files generated within the specified time frame
    """
    filteredFiles = []
    timeDiff = date.today() - timedelta(days)

    for f in files:
        if 'CLOSED' in f:
            continue
        # grab date portion of file to compare (truncate .xlsx)
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
    
    frames = [pd.read_excel(f, index_col=None, engine='openpyxl', usecols="A,C") for f in files]
    combinedFiles = pd.concat(frames)
    return combinedFiles
    
def writeToExcelIndustry(indData, days) -> None:
    """
    method to write the frequency in which each industry appears in the past {days} into an excel file 
    
    :param indData: dictionary containing industries and count of each
    :param days: number of days to analyze data over
    :return: none
    """

    currDay = date.today()
    fileName = "past-" + str(days) + "-days-" + str(currDay) + '.xlsx'
    path = 'analytics/industries/' + fileName

    # worksheet set up
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})

    formatToFromHeader(worksheet, days, bold)
    worksheet.write(3,0, 'Industry', bold)
    worksheet.write(3,1, 'Frequency', bold)

    row,col = 4, 0

    for key in indData:
        worksheet.write_string(row, col, key)
        worksheet.write_number(row, col+1, indData[key])
        row += 1

    workbook.close()

def writeToExcelTickers(tickerData, days) -> None:
    """
    method to write ticker data grouped by industry into an excel file 
    
    :param tickerData: dictionary containing industries and respective tickers
    :param days: number of days to analyze data over
    :return: none
    """
    
    currDay = date.today()
    fileName = "past-" + str(days) + "-days-" + str(currDay) + '.xlsx'
    path = 'analytics/tickers/' + fileName

    # worksheet set up
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})

    formatToFromHeader(worksheet, days, bold)
    worksheet.write(3,0, 'Industry', bold)
    worksheet.write(3,1, 'Tickers', bold)

    row,col = 4, 0

    for key in tickerData:
        worksheet.write_string(row, col, key)
        worksheet.write_string(row, col+1, ", ".join(tickerData[key]))
        row += 1

    workbook.close()

def formatToFromHeader(worksheet, days, format):
    """
    format excel To / From headers. kinda sketch tbh 
    
    :param worksheet: the worksheet to add To / From headers
    :param days: number of days to analyze data over
    :param format: format for particular cell (i.e. bold etc.) 
    :return: none
    """
    currDay = str(date.today())
    startDay = str(date.today() - timedelta(days))
    worksheet.write(0,0,'From', format)
    worksheet.write(0,1, 'To', format)
    worksheet.write(1,0, startDay)
    worksheet.write(1,1, currDay)
    worksheet.set_column(0, 0, len(currDay)+2)
    worksheet.set_column(0, 1, len(startDay)+2)
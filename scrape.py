import requests
import re

from bs4 import BeautifulSoup
from scrapeUtil import getColWidth, writeToExcel, reminder
 
# general setup 
# we will target Finviz top gainers table (LHS of FINVIZ home page)
url = "https://www.finviz.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find('table', class_='t-home-table')

data = []
tblHeaders = ['Ticker', 'Change %', 'Industry', 'Company Name', 'Country', 'Market Cap'] # TODO: update to grab headers from site
colWidths = getColWidth(tblHeaders)

# scrape data in top gainers table
for idx, stock in enumerate(table):

    # data is available for even number elements > 0
    if idx % 2 == 0 and idx != 0:
        ticker = stock.find('a').get_text()
        change = stock.find('span')
        if change is None:
            change = '0.00%'
        else:
            change = change.get_text()
        ticker_info = stock.find('td')
        companySearch = re.search(r'(?<=\b&gt;)(.*?)(?=\&lt)', str(ticker_info))
        company = companySearch.group(0)
        hoverSearch = re.search(r'(?<=\;br&gt;\s)(.*?)(?=\])', str(ticker_info))
        hover = hoverSearch.group(0).replace('&amp; ', '')
        hover = hover.split('|')
        data.append([ticker, change, company, hover[0], hover[1], hover[2]])

        if len(company) > colWidths[3]:
            colWidths[3] = len(company)
        if len(hover[0]) > colWidths[2]:
            colWidths[2] = len(hover[0])

# write data to excel file
writeToExcel(data, tblHeaders, colWidths)
reminder()
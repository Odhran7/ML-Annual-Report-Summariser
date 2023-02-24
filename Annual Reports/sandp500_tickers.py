# A function that returns an array of the S and P 500 CIKS
import bs4 as bs
import requests

# Returns a list of the S & P 500 tickers in an array called tickers using web scraping from a Wikipedia website 

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker[:-1])
    return tickers

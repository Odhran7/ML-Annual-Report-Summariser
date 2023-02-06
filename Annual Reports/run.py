from pre_process import remove_stopwords_and_tokenize, annual_report_items, get_text
from reports import base_query, get_urls_for_ticker
from sandp500_tickers import save_sp500_tickers
from sec_api import QueryApi
from sec_api import ExtractorApi

# Setting API keys

api_key = "b8113d497aa775cb50186f7f03c97c7e8b3158734705787264d31e7f627dc6db"

# Getting all the tickers from the S and P 500

tickers = save_sp500_tickers()

# Creating a new instance of the queryapi & extractorApi

queryapi = QueryApi(api_key)
extractorApi = ExtractorApi(api_key)

# Getting all annual reports for s and p 500
# Note: Running this will download all available annual reports from the ticker list: S&P500
# Will also do some minor text pre-processing 

for ticker in tickers:
    get_urls_for_ticker(base_query, ticker, 2000, 2022)
    path = './urls/' + ticker + '_urls.txt'
    get_text(path, annual_report_items)


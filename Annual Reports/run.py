
from reports import get_10k_URLS_for_particular_company
from extracting_sections_and_preprocessing import get_section
from extracting_sections_and_preprocessing import remove_stopwords_and_tokenize
from sandp500_tickers import save_sp500_tickers

annual_report_itmes = ["1","1A","1B","2","3","4","7","9","9A","9B","10","11","12","13","14"]

tickers = save_sp500_tickers()


for ticker in tickers:
    get_10k_URLS_for_particular_company(2020,2017,ticker)
    path = './urls/' + ticker + '_urls.txt'
    get_section(path,annual_report_itmes)

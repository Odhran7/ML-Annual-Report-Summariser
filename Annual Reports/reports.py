# Download 10ks to local machine 

from sandp500_tickers import save_sp500_tickers
from sec_api import QueryApi
import json 

def get_10k_URLS_for_particular_company(start, end,ticker):
  api_key = "161be08b7c1b9d92a04867c50069b622edcc8716ee151ae6929c571d9e3689c3"

  #tickers = save_sp500_tickers()

# Creating a new instance of the queryapi 

  

  queryApi = QueryApi(api_key)

  query = {
  "query": { "query_string": { 
      "query": "ticker:AAPL AND filedAt:[2020-01-01 TO 2021-12-31] AND formType:\"10-K\"",
      "time_zone": "America/New_York"
  } },
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
}

  response = queryApi.get_filings(query)

  
  

  log_file = open("filing_urls.txt", "a")

# start with filings filed in 2021, then 2020, 2019, ... up to 2010 
# uncomment line below to fetch all filings filed in 2022-2010
# for year in range(2021, 2009, -1):
  for year in range(start, end, -1):
    print("starting {year}".format(year=year))
  
  # a single search universe is represented as a month of the given year
    
    # get 10-Q and 10-Q/A filings filed in year and month
    # resulting query example: "formType:\"10-Q\" AND filedAt:[2021-01-01 TO 2021-01-31]"
    universe_query = \
    "ticker:{ticker} AND "+ \
    "filedAt:[{year}-01 TO {year}-31] AND" \
    "formType:\"10-K\""
    universe_query.format(ticker = ticker)
    universe_query.format(year=year)
  
    print(universe_query)
    # set new query universe for year-month combination
    query["query"]["query_string"]["query"] = universe_query;

    # paginate through results by increasing "from" parameter 
    # until we don't find any matches anymore
    # uncomment line below to fetch 10,000 filings
    # for from_batch in range(0, 9800, 200): 
    

      # for each filing, only save the URL pointing to the filing itself 
      # and ignore all other data. 
      # the URL is set in the dict key "linkToFilingDetails"
    urls_list = list(map(lambda x: x["linkToFilingDetails"], response["filings"]))

      # transform list of URLs into one string by joining all list elements
      # and add a new-line character between each element.
    urls_string = "\n".join(urls_list) + "\n"
      
    log_file.write(urls_string)




  log_file.close()

get_10k_URLS(2022,2021,"AAPL")

import os
import multiprocessing

def download_all_filings():
  print("Start downloading all filings")

  download_folder = "./filings" 
  if not os.path.isdir(download_folder):
    os.makedirs(download_folder)
    
  # uncomment next line to process all URLs
  # urls = load_urls()
  urls = load_urls()[1:40]
  print("{length} filing URLs loaded".format(length=len(urls)))

  number_of_processes = 20

  with multiprocessing.Pool(number_of_processes) as pool:
    pool.map(download_filing, urls)
  
  print("All filings downloaded")
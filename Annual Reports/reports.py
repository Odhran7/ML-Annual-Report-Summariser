# Download 10ks to local machine 

from sandp500_tickers import save_sp500_tickers
from sec_api import QueryApi
import json 

def get_10k_URLS_for_particular_company(start, end,ticker):
  api_key = "b8113d497aa775cb50186f7f03c97c7e8b3158734705787264d31e7f627dc6db"
  queryApi = QueryApi(api_key)
  query = {
  "query": { "query_string": { 
      #"query": "ticker:AAPL AND filedAt:[2020-01-01 TO 2020-12-31] AND formType:\"10-K\"",
      "query": "ticker:AAPL AND filedAt:[2021-01-01 TO 2021-12-31] AND formType:\"10-K\"",
      "time_zone": "America/New_York"
  } },
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
}
  log_file = open("filing_urls.txt", "a")
  


  for year in range(start, end, -1):
    print("starting {year}".format(year=year))
  
  
    universe_query = "ticker:{ticker} AND ".format(ticker = ticker)+\
    "filedAt:[{year}-01-01 TO {year}-12-31] AND ".format(year = year)+\
    "formType:\"10-K\"" 
    
    
  
    
    
    query["query"]["query_string"]["query"] = universe_query;
    
    response = queryApi.get_filings(query)
    

    
    

      
    urls_list = list(map(lambda x: x["linkToFilingDetails"], response["filings"]))
    
      
    log_file.write(urls_list[-1]+"\n")




  log_file.close()



get_10k_URLS_for_particular_company(2022,2000,"TSLA")



def get_section(path, item): 
    file = open(path, 'r')
    lines = file.readlines()
    output_file = open(path[:-3] + "_{item}.txt".format(item = item), 'a')
    for url in lines:
      print(url)
      section_text = extractorApi.get_section(url, item, "text")
      output_file.write(section_text + "\n\n\n")
    output_file.close()
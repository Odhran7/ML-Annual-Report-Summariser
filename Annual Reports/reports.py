# Download 10ks to local machine 


from sec_api import QueryApi




api_key = "b8113d497aa775cb50186f7f03c97c7e8b3158734705787264d31e7f627dc6db"
def get_10k_URLS_for_particular_company(start, end,ticker):
  
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
  log_file = open('./urls/{ticker}_urls.txt'.format(ticker = ticker), 'a')
  


  for year in range(start, end, -1):
    #print("starting {year}".format(year=year))
  
  
    universe_query = "ticker:{ticker} AND ".format(ticker = ticker)+\
    "filedAt:[{year}-01-01 TO {year}-12-31] AND ".format(year = year)+\
    "formType:\"10-K\"" 
    
    
  
    
    
    query["query"]["query_string"]["query"] = universe_query;
    
    response = queryApi.get_filings(query)
    

    
    

      
    urls_list = list(map(lambda x: x["linkToFilingDetails"], response["filings"]))
    
    if(len(urls_list)==0):
      print("No annual report for {year}, breaking out ".format(year = year))
      break  
    log_file.write(urls_list[-1]+"\n")




  log_file.close()



#get_10k_URLS_for_particular_company(2022,2000,"MCD")



 



  


#preprocess_textfile('./TSLA_urls.txt')
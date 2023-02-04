from sec_api import ExtractorApi
from bs4 import BeautifulSoup
from sandp500_tickers import save_sp500_tickers


api_key = "b8113d497aa775cb50186f7f03c97c7e8b3158734705787264d31e7f627dc6db"
annual_report_itmes = ["1","1A","1B","2","3","4","7","9","9A","9B","10","11","12","13","14"]
extractorApi = ExtractorApi(api_key)
import string 

import re
def get_section(path, list_items): 
  file = open(path, 'r', encoding = 'utf-8')
  lines = file.readlines()
  output_file = open('./content/' + path[7:-8] + ".txt", 'a', encoding = 'utf-8')
  for url in lines:
    print(url)
    for item in list_items:
      print("Adding item:{item} to .txt file".format(item = item))
      section_text = extractorApi.get_section(url, item, "text").lower()
      soup = BeautifulSoup(section_text, "html.parser")
      section_text_without_html = soup.get_text()
      translator = str.maketrans('', '', string.punctuation)
      section_text_without_html = section_text_without_html.translate(translator)
      new_text = re.sub(r'tablestart.*?tableend', '', section_text_without_html, flags=re.DOTALL)
      output_file.write(new_text + "\n\n\n")
  output_file.close()

#get_section('MCD_urls.txt', '7')


def get_sections_for_companies(company_tickers,item):
  company_tickers = save_sp500_tickers()
  for ticker in company_tickers:
    get_section('./{ticker}_urls.txt'.format(ticker = ticker),item = item)

import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')



def remove_stopwords_and_tokenize(path):
  file = open(path, 'r')
  lines = file.read()
  #output_file = open(path[:-4] + "_preprocessed.txt", 'w')
  
  stop_words = set(stopwords.words("english"))
  words = nltk.word_tokenize(lines)
  
  words = [word for word in words if word not in stop_words]

  print(words)
  #output_file.write("".join(words))
 # output_file.close()

  #filtered_text = [[word for word in line if word not in stop_words]for line in lines]

#remove_stopwords_and_tokenize('NFLX__7.txt')
import re
from bs4 import BeautifulSoup
from sec_api import ExtractorApi, QueryApi
import string

api_key = "b8113d497aa775cb50186f7f03c97c7e8b3158734705787264d31e7f627dc6db"

queryapi = QueryApi(api_key)
extractorApi = ExtractorApi(api_key)

''' 
1 - Business
1A - Risk Factors
1B - Unresolved Staff Comments
2 - Properties
3 - Legal Proceedings
4 - Mine Safety Disclosures
5 - Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities
6 - Selected Financial Data (prior to February 2021)
7 - Management’s Discussion and Analysis of Financial Condition and Results of Operations
7A - Quantitative and Qualitative Disclosures about Market Risk
8 - Financial Statements and Supplementary Data
9 - Changes in and Disagreements with Accountants on Accounting and Financial Disclosure
9A - Controls and Procedures
9B - Other Information
10 - Directors, Executive Officers and Corporate Governance
11 - Executive Compensation
12 - Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters
13 - Certain Relationships and Related Transactions, and Director Independence
14 - Principal Accountant Fees and Services
'''
# Getting the clean-text of an item (see above) for the list of urls in a .txt file located at path ad preprocesses it by applying lowercase
# and removes the HTML tags, punctuation, and tables located in the text file

def get_section(path, item): 
    file = open(path, 'r', encoding='utf-8')
    lines = file.readlines()
    output_file = open(path[:-4] + "_{item}.txt".format(item = item), 'a')
    for url in lines:
      print(url)
      
      section_text = extractorApi.get_section(url, item, "text").lower()
      
      soup = BeautifulSoup(section_text, "html.parser")
      section_text_without_html = soup.get_text()
      translator = str.maketrans('', '', string.punctuation)
      section_text_without_html = section_text_without_html.translate(translator)
      new_text = re.sub(r'tablestart.*?tableend', '', section_text_without_html, flags=re.DOTALL)
      
      
      output_file.write(new_text + "\n\n\n")
    output_file.close()

# Apostrophes not gone 

# get_section('./TSLA.txt', '7')

import nltk
from nltk.corpus import stopwords

# Donwloading the stop words 

# nltk.download("stopwords")
# nltk.download('punkt')

# Opens file located in path and removes stopwords such as 'the' and 'and' etc. and tokenizes the remaining words and applies stemming and prints to console

def remove_stopwords_and_tokenize(path):
  file = open(path, 'r')
  lines = file.read()  
  stop_words = set(stopwords.words("english"))
  words = nltk.word_tokenize(lines)
  words = [word for word in words if word not in stop_words]
  print(words)



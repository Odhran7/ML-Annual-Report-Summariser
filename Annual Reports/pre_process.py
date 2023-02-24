import re
from bs4 import BeautifulSoup
from sec_api import ExtractorApi, QueryApi
import string

# Setting the API Key 

api_key = "b8113d497aa775cb50186f7f03c97c7e8b3158734705787264d31e7f627dc6db"

# Instantiating the sec query api 

queryapi = QueryApi(api_key)

# Instantiating the sec query extractor api 

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

# Defining an array with all the parts relevant to summarisation

annual_report_items = ['1', '1A', '1B', '2', '3', '4', '5', '7', '7A', '9', '9A', '9B', '10', '11', '12', '13', '14']

# Getting the clean-text of an item (see above) for the list of urls in a .txt file located at path ad preprocesses it by applying lowercase
# and removes the HTML tags, punctuation, and tables located in the text file

def get_text(path, list_items):

  # Opens file with attribute read and encoding utf-8

  file = open(path, 'r', encoding = 'utf-8')

  # Open files and read lines from stream

  lines = file.readlines()

  # Creates output file in the content directory with ticker name.txt

  output_file = open('./content/' + path[7:-8] + ".txt", 'a', encoding = 'utf-8')

  # For each URL in the input stream (lines)

  for url in lines:
    print(url)

  # For each item in list_items (all the annual report items that we deem neccessary for summarization)

    for item in list_items:
      print("Adding item:{item} to .txt file".format(item = item))

      # Using the extractor api to get the section 

      section_text = extractorApi.get_section(url, item, "text")

      # Creating a BS object so we can pre-process the data

      soup = BeautifulSoup(section_text, "html.parser")

      # Removes the html

      section_text_without_html = soup.get_text()

      # Removes the punctuation 

      # translator = str.maketrans('', '', string.punctuation)
      # section_text_without_html = section_text_without_html.translate(translator)

      # Gets rid of all tables ie financial documents 

      new_text = re.sub(r'tablestart.*?tableend', '', section_text_without_html, flags=re.DOTALL)

      # Write each section to the output file separated with three new line characters

      output_file.write(new_text + "\n\n\n")

  # Close the stream

  output_file.close()

# get_section('./TSLA.txt', '7')

import nltk
from nltk.corpus import stopwords

# Donwloading the stop words 

# nltk.download("stopwords")
# nltk.download('punkt')

# Opens file located in path and removes stopwords such as 'the' and 'and' etc. and tokenizes the remaining words and applies stemming and prints to console

def remove_stopwords_and_tokenize(path):

  # Opens the file with attribute read

  file = open(path, 'r')

  # Read the lines from lines

  lines = file.read()  

  # Reads all the stop words from the nltk library

  stop_words = set(stopwords.words("english"))

  # Tokenise the lines

  words = nltk.word_tokenize(lines)

  # Create an array of sentences without the stop words 

  words = [word for word in words if word not in stop_words]

  # Print the array of words without the stop words

  print(words)



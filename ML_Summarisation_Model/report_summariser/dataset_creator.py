import pandas as pd 
from datasets import Dataset
import os 

def load_data(directory):
    data_dict = { "document": [], "summary": []}

    # Loop over all CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            path = os.path.join(directory, filename)
            df = pd.read_csv(path, header= None, names=["documents", "summaries"], usecols=[0,1])
            
            texts = df["documents"].astype(str)
            summaries = df["summaries"].astype(str)
            
            
            
            
            # Append the data from the current CSV file to the data_dict
            
            data_dict["document"].extend(texts)
            data_dict["summary"].extend(summaries)
    
    dataset = Dataset.from_dict(data_dict)
    dataset = dataset.train_test_split(train_size=0.9)
    return dataset
data = load_data("ML_Summarisation_Model\Training\Summaries\Item 1A - Risk Factors\A")
print(data)


'''
def load_data(path):
    df = pd.read_csv(path,header=None, names=["row","documents","summaries"])
    texts = df["documents"].astype(str)
    
    summaries = df["summaries"].astype(str)
    ids = df["row"].astype(str)
    data_dict = {"id":ids,"documents":texts,"summaries":summaries}
    dataset = Dataset.from_dict(data_dict)
    dataset = dataset.train_test_split(train_size=0.9)
    return dataset

data =load_data("ML_Summarisation_Model/Training/Summaries/Item 1A - Risk Factors/A/A_Item_1A_Document_Summary - Sheet1.csv")
'''
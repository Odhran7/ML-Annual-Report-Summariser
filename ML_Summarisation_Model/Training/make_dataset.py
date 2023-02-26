import os
from datasets import Dataset
import pandas as pd

# This function creates a Hugging Face dataset with cols id, document, summary whereby summaries are the labels. It returns the train/test subsets @ 0.8. It only does this for the first 10 annual reports






def loadData():
    df = pd.read_csv('ML_Summarisation_Model\Training\Summaries\Item 1A - Risk Factors\A\A_Item_1A_Document_Summary - Sheet1.csv', header=None, names=["row", 'document', 'summary'],encoding="utf-8")
    print(df.head())
    texts = df["document"].astype(str)
    summaries = df["summary"].astype(str)
    ids = df['row'].astype(str)
    data_dict = {"id":ids,"documents":texts,"summaries":summaries}
    
    
    dataset = Dataset.from_dict(data_dict)
    dataset = dataset.train_test_split(train_size=0.8,)
    

    return dataset
dataset = loadData()
print(dataset)





def loadData():
    df = pd.read_csv('ML_Summarisation_Model\Training\Summaries\Item 1A - Risk Factors\A\A_Item_1A_Document_Summary - Sheet1.csv', header=None, names=["row", 'document', 'summary'],encoding="utf-8")
    print(df.head())
    texts = df["document"].astype(str)
    summaries = df["summary"].astype(str)
    ids = df['row'].astype(str)
    data_dict = {"id":ids,"documents":texts,"summaries":summaries}
    
    
    dataset = Dataset.from_dict(data_dict)
    dataset = dataset.train_test_split(train_size=0.8,)
    

    return dataset
dataset = loadData()
print(dataset)


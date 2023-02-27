import pandas as pd 
from datasets import Dataset


def loadData(path):
    df = pd.read_csv(path,header=None, names=["row","documents","summaries"])
    texts = df["documents"].astype(str)
    summaries = df["summaries"].astype(str)
    ids = df["row"].astype(str)
    data_dict = {"id":ids,"documents":texts,"summaries":summaries}
    dataset = Dataset.from_dict(data_dict)
    dataset = dataset.train_test_split(train_size=0.9)
    return dataset

print(loadData("ML_Summarisation_Model/Training/Summaries/Item 1A - Risk Factors/A/A_Item_1A_Document_Summary - Sheet1.csv"))

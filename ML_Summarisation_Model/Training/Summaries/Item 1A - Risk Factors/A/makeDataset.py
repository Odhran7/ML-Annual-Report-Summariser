from datasets import Dataset
import pandas as pd


def loadData(path):
    df = pd.read_csv(path
                     ,header=None,names=["row","documents","summaries"])
    ids = df["row"].astype(str)
    documents = df["documents"].astype(str)
    summaries = df["summaries"].astype(str)
    data_dict = {"ids":ids,"documents":documents,"summaries":summaries}
    dataset = Dataset.from_dict(data_dict)
    dataset = dataset.train_test_split(train_size=0.9)
    return dataset

dataset = loadData("ML_Summarisation_Model\Training\Summaries\Item 1A - Risk Factors\A\A_Item_1A_Document_Summary - Sheet1.csv")
print(dataset)
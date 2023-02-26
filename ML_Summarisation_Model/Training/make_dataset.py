import os
from datasets import Dataset
import pandas as pd 

# This function creates a Hugging Face dataset with cols id, document, summary whereby summaries are the labels. It returns the train/test subsets @ 0.8. It only does this for the first 10 annual reports
'''
def load_data():
    train_data = []
    label_summaries = []

    import os 
    for count,annualReport in enumerate(os.listdir("content")):

        # Gets the first 10 annual reports that we listed in content folder (sorted alphabetically)

        if count>10:
         break
        file_path = os.path.join("content", annualReport)
        with open(file_path,"r",encoding = "utf-8") as f:
            document = f.read()

        # Only appends the first 100 characters

            train_data.append(document[:100])

        # Sets labels to same thing (just for testing purposes)

    for count,summary in enumerate(os.listdir("content")):
        if count>10:
         break
        file_path = os.path.join("content", summary)
        with open(file_path,"r",encoding = "utf-8") as f:
            summary = f.read()
    
        # Only appends the first 100 characters

            label_summaries.append(summary[:100])

    # Converts train array and label array to HuggingFace dataset object 

    dataset = Dataset.from_dict({"doc":train_data,"sum":label_summaries})

    # Converts dataset into train and test subsets using train size of 0.8. Ideally, we would have a validation set

    dataset_train_test = dataset.train_test_split(train_size=0.8,)

    # Returns the split dataset object
    
    return dataset_train_test


'''

def read_csv(path):
    df = pd.read_csv(path, header=None)
    print(df.tail)

read_csv("ML_Summarisation_Model/Training/Summaries/Item 1A - Risk Factors/A/A_Item_1A_Document_Summary - Sheet1.csv")

from make_dataset import load_data
from finetuned_model import train, test, summarise, test_compete
from compete_model import summarise_compete

# This file is used to run the training on the model and save the model 


# Trains the model and prints out the ROUGE scores (note will overfit the model)

trainer = train()

# Uncomment to calculate metrics on the test set 

# test()

# Call this to summarise

document = ""
summarise(document)

# Call this to summarise the compete model

document_compete = ""
summarise_compete(document_compete)

# Calculate the metrics on the compete model

test_compete()


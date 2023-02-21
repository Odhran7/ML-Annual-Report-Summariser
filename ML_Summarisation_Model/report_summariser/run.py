from report_summariser import load_data
from Pegasus_finetune import train

# Import the dataset
huggingface_dict = load_data()


# Trains the model

trainer = train()

# Calculate the metrics

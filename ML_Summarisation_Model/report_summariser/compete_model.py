from transformers import PegasusTokenizer, pipeline

# This is the model we are going to compare ours against. This model summarises financial news articles

# Generating a summary using the compete model 

def summarise_compete(document):

    # Setting the model name of the compete model

    model_name = "human-centered-summarization/financial-summarization-pegasus"

    # Setting the tokenizer for the compete model

    tokenizer = PegasusTokenizer.from_pretrained(model_name)

    # Creating the compete model using the compete model name

    model = pipeline("summarization", model_name, tokenizer=tokenizer)

    # Generating the summary from the given document 

    summary = model(document)

    # Return the summary

    return summary
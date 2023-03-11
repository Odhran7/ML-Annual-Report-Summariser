from transformers import pipeline

model_name = "google/pegasus-large"

    # Setting the tokenizer for the compete model



def magic(text):
    model = pipeline("summarization",model = model_name)
    

    summary = model(text)

    return summary
from tqdm import tqdm
import torch

# This calculates and returns teh ROUGE score of a summarisation model

def calculate_metric_on_test_ds(dataset, metric, model, tokenizer, 
                               batch_size=16, device = "cuda" if torch.cuda.is_available() else "cpu", 
                               column_text="article", 
                               column_summary="highlights"):
    article_batches = list(generate_batch_sized_chunks(dataset[column_text], batch_size))
    target_batches = list(generate_batch_sized_chunks(dataset[column_summary], batch_size))

    for article_batch, target_batch in tqdm(
        zip(article_batches, target_batches), total=len(article_batches)):
        
        inputs = tokenizer(article_batch, max_length=1024,  truncation=True, 
                        padding="max_length", return_tensors="pt")
        
        summaries = model.generate(input_ids=inputs["input_ids"].to(device),
                         attention_mask=inputs["attention_mask"].to(device), 
                         length_penalty=0.8, num_beams=8, max_length=128)

        ''' parameter for length penalty ensures that the model does not generate sequences that are too long. '''
        
        # Finally, we decode the generated texts, 

        # Replace the  token, and add the decoded texts with the references to the metric.

        decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True, 
                                clean_up_tokenization_spaces=True) 
               for s in summaries]      
        
        decoded_summaries = [d.replace("", " ") for d in decoded_summaries]
        
        
        metric.add_batch(predictions=decoded_summaries, references=target_batch)
        
    #  Finally compute and return the ROUGE scores.

    score = metric.compute()
    return score

#  Split the dataset into smaller batches that we can process simultaneousl Yield successive batch-sized chunks from list_of_elements.

def generate_batch_sized_chunks(list_of_elements, batch_size):

    for i in range(0, len(list_of_elements), batch_size):
        yield list_of_elements[i : i + batch_size]
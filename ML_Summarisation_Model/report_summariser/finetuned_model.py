from transformers import PegasusForConditionalGeneration, PegasusTokenizer, Trainer, TrainingArguments, AutoTokenizer
import torch
from rouge_calculator import calculate_metric_on_test_ds
import pandas as pd
from datasets import load_metric
from transformers import pipeline 
from dataset_creator import load_data

pathToTrainingDirectory = "ML_Summarisation_Model\Training\Summaries\Item 1A - Risk Factors\A"
# This class is used to fine tune a pre-existing model. We are going to apply this to the pre-trained Pegasus model - in particular the Pegasus Large model

class PegasusDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels['input_ids'][idx])  
        return item
    def __len__(self):
        return len(self.labels['input_ids'])  

      
def prepare_data(model_name, 
                 train_texts, train_labels, 
                 val_texts=None, val_labels=None, 
                 test_texts=None, test_labels=None):
  """
  Prepare input data for model fine-tuning
  """
  tokenizer = PegasusTokenizer.from_pretrained(model_name)

  prepare_val = False if val_texts is None or val_labels is None else True
  prepare_test = False if test_texts is None or test_labels is None else True

  def tokenize_data(texts, labels):
    encodings = tokenizer(texts, truncation=True, padding=True)
    decodings = tokenizer(labels, truncation=True, padding=True)
    dataset_tokenized = PegasusDataset(encodings, decodings)
    return dataset_tokenized

  train_dataset = tokenize_data(train_texts, train_labels)
  val_dataset = tokenize_data(val_texts, val_labels) if prepare_val else None
  test_dataset = tokenize_data(test_texts, test_labels) if prepare_test else None

  return train_dataset, val_dataset, test_dataset, tokenizer


def prepare_fine_tuning(model_name, tokenizer, train_dataset, val_dataset=None, freeze_encoder=False, output_dir='./results'):
  """
  Prepare configurations and base model for fine-tuning
  """
  torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
  model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

  if freeze_encoder:
    for param in model.model.encoder.parameters():
      param.requires_grad = False

  if val_dataset is not None:
    training_args = TrainingArguments(
      output_dir=output_dir,           # output directory
      num_train_epochs=2000,           # total number of training epochs
      per_device_train_batch_size=1,   # batch size per device during training, can increase if memory allows
      per_device_eval_batch_size=1,    # batch size for evaluation, can increase if memory allows
      save_steps=500,                  # number of updates steps before checkpoint saves
      save_total_limit=5,              # limit the total amount of checkpoints and deletes the older checkpoints
      evaluation_strategy='steps',     # evaluation strategy to adopt during training
      eval_steps=100,                  # number of update steps before evaluation
      warmup_steps=500,                # number of warmup steps for learning rate scheduler
      weight_decay=0.01,               # strength of weight decay
      logging_dir='./logs',            # directory for storing logs
      logging_steps=10,
    )

    trainer = Trainer(
      model=model,                         # the instantiated Transformers model to be trained
      args=training_args,                  # training arguments, defined above
      train_dataset=train_dataset,         # training dataset
      eval_dataset=val_dataset,            # evaluation dataset
      tokenizer=tokenizer
    )

  else:
    training_args = TrainingArguments(
      output_dir=output_dir,           # output directory
      num_train_epochs=2000,           # total number of training epochs
      per_device_train_batch_size=1,   # batch size per device during training, can increase if memory allows
      save_steps=500,                  # number of updates steps before checkpoint saves
      save_total_limit=5,              # limit the total amount of checkpoints and deletes the older checkpoints
      warmup_steps=500,                # number of warmup steps for learning rate scheduler
      weight_decay=0.01,               # strength of weight decay
      logging_dir='./logs',            # directory for storing logs
      logging_steps=10,
    )

    trainer = Trainer(
      model=model,                         # the instantiated Transformers model to be trained
      args=training_args,                  # training arguments, defined above
      train_dataset=train_dataset,         # training dataset
      tokenizer=tokenizer
    )

  return trainer

# The train function will return the trained model on our custom annual report dataset and returns the trained trainer object

def train():

  # This loads our custom function used to create a train/test dataset using excerpts and labelled summaries as the datatypes

    dataset = load_data(pathToTrainingDirectory)

  # Splits the data into the train excerpts and the summaries from the preloaded dataeset 

    train_texts, train_labels = dataset['train']['document'][:1000], dataset['train']['summary'][:1000]
    print(dataset)

    # use Pegasus Large model as base for fine-tuning

    model_name = 'google/pegasus-large'

    # Prepares the data for fine-tuning

    train_dataset, _, _, tokenizer = prepare_data(model_name, train_texts, train_labels)
    trainer = prepare_fine_tuning(model_name, tokenizer, train_dataset)

    # Trains the model

    trainer.train()

    # Setting model variable to the model attribute of the trainer object 

    model = trainer.model

    # Saving the fine-tuned model locally so we can load it back up using one line for generating and testing

    model.save_pretrained("pegasus-annualreport-model")

    # Save the tokenizer as well as we need to use the tokenizer to tokenize and encode the individual words

    tokenizer.save_pretrained("tokenizer")

    # Loads the rouge metric library

    rouge_metric = load_metric('rouge')

    # Score calculates the ROUGE metric on the train data

    score = calculate_metric_on_test_ds(dataset['train'], rouge_metric, model, tokenizer, column_text = 'document', column_summary='sum')

    # ROUGE1: Recall (amount of words in summary that are in the document) Orientated Understudy for Gisting Evaluation by subset one word
    # ROUGE2: Recall (amount of words in summary that are in the document) Orientated Understudy for Gisting Evaluation by subset two words
    # ROUGEL: Recall (amount of words in summary that are in the document) Orientated Understudy for Gisting Evaluation by the longest common subsequence 
    # ROUGE1: Recall (amount of words in summary that are in the document) Orientated Understudy for Gisting Evaluation by the set of unique n-consecutive words that are present in both the machine generated summary and the original doucment

    rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

    # Puts the scores in the dictionary

    rouge_dict = dict((rn, score[rn].mid.fmeasure ) for rn in rouge_names )

    # Prints the sores in a pandas dataframe

    print(pd.DataFrame(rouge_dict, index = ['pegasus']))

    # Returns the new trainer object

    return trainer

# This returns the rouge scores on the test set

def test():

  # Loading the pre-trained tokenizer

  tokenizer = AutoTokenizer.from_pretrained("tokenizer")

  # Loads the pre-trained model

  model = PegasusForConditionalGeneration.from_pretrained("pegasus-annualreport-model")

  # Load the ROUGE metric library

  rouge_metric = load_metric('rouge')

  # Loading our custom dataset 

  dataset = load_data()

  # Score calculates the ROUGE metric on the train data

  score = calculate_metric_on_test_ds(dataset['test'], rouge_metric, model, tokenizer, column_text = 'document', column_summary='sum')

  # ROUGE1: Recall (amount of words in summary that are in the document) Orientated Understudy for Gisting Evaluation by subset one word
  # ROUGE2: Recall (amount of words in summary that are in the document) Orientated Understudy for Gisting Evaluation by subset two words
  # ROUGEL: Recall (amount of words in summary that are in the document) Orientated Understudy for Gisting Evaluation by the longest common subsequence 
  # ROUGE1: Recall (amount of words in summary that are in the document) Orientated Understudy for Gisting Evaluation by the set of unique n-consecutive words that are present in both the machine generated summary and the original doucment

  rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

  # Puts the scores in the dictionary

  rouge_dict = dict((rn, score[rn].mid.fmeasure ) for rn in rouge_names )

  # Prints the sores in a pandas dataframe

  print(pd.DataFrame(rouge_dict, index = ['pegasus']))


# Using the pipeline API to summarise a given document using our fine-tuned model

def summarise(document):
  
  # Loading the pre-trained tokenizer to use the pipeline API

  tokenizer = AutoTokenizer.from_pretrained("tokenizer")

  # Instantiate the pipeline object

  model = pipeline("summarization", "pegasus-annualreport-model", tokenizer=tokenizer)

  # Generating the summary from the given document 

  summary = model(document)

  # Return the summary text

  return summary


# This function returns the ROUGE metrics for the compete_model 

def test_compete():

  # Setting the model name of the compete model

  model_name = "human-centered-summarization/financial-summarization-pegasus"

  # Setting the tokenizer of the compete model

  tokenizer = PegasusTokenizer.from_pretrained(model_name)

  # Load the ROUGE metric library

  rouge_metric = load_metric('rouge')

  # Loading our custom dataset 

  dataset = load_data()

  # Score calculates the ROUGE metric on the train data

  score = calculate_metric_on_test_ds(dataset['test'], rouge_metric, model_name, tokenizer, column_text = 'document', column_summary='sum')

  # ROUGE1: Recall (amount of words in summary that are in the document) Orientated Understudy for Gisting Evaluation by subset one word
  # ROUGE2: Recall (amount of words in summary that are in the document) Orientated Understudy for Gisting Evaluation by subset two words
  # ROUGEL: Recall (amount of words in summary that are in the document) Orientated Understudy for Gisting Evaluation by the longest common subsequence 
  # ROUGE1: Recall (amount of words in summary that are in the document) Orientated Understudy for Gisting Evaluation by the set of unique n-consecutive words that are present in both the machine generated summary and the original doucment

  rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

  # Puts the scores in the dictionary

  rouge_dict = dict((rn, score[rn].mid.fmeasure ) for rn in rouge_names )

  # Prints the sores in a pandas dataframe

  print(pd.DataFrame(rouge_dict, index = ['pegasus']))


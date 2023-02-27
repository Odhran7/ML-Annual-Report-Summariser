import sagemaker
import boto3

iam_client = boto3.client('iam')
role = iam_client.get_role(RoleName='localAccessToSage')['Role']['Arn']
sagemaker_session_bucket = "jimsbin"
sess = sagemaker.Session(default_bucket=sagemaker_session_bucket)


import transformers
import datasets
import argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # hyperparameters sent by the client are passed as command-line arguments to the script
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--per_device_train_batch_size", type=int, default=32)
    parser.add_argument("--model_name_or_path", type=str)

    # data, model, and output directories
    parser.add_argument("--model-dir", type=str, default=os.environ["SM_MODEL_DIR"])
    parser.add_argument("--training_dir", type=str, default=os.environ["SM_CHANNEL_TRAIN"])
    parser.add_argument("--test_dir", type=str, default=os.environ["SM_CHANNEL_TEST"])


from sagemaker.huggingface import HuggingFace


# hyperparameters which are passed to the training job
hyperparameters={'epochs': 1,
                 'per_device_train_batch_size': 32,
                 'model_name_or_path': 'google/pegasus-large'
                 }

# create the Estimator
huggingface_estimator = HuggingFace(
        entry_point='train.py',
        source_dir='./scripts',
        instance_type='ml.p3.2xlarge',
        instance_count=1,
        role=role,
        transformers_version='4.4',
        pytorch_version='1.6',
        py_version='py36',
        hyperparameters = hyperparameters
)

huggingface_estimator.fit(
  {'train': 's3://sagemaker-us-east-1-558105141721/samples/datasets/imdb/train',
   'test': 's3://sagemaker-us-east-1-558105141721/samples/datasets/imdb/test'}
)
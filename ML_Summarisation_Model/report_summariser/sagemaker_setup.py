import sagemaker
import boto3

iam_client = boto3.client('iam')
role = iam_client.get_role(RoleName='localAccessToSage')['Role']['Arn']
sagemaker_session_bucket = "jimsbin"
sess = sagemaker.Session(default_bucket=sagemaker_session_bucket)

from dataset_creator import load_data

data = load_data("ML_Summarisation_Model\Training\Summaries\Item 1A - Risk Factors\A")



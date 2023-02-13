from datasets import load_dataset
import datasets
import List


# Loading the test data

# load_dataset('report_summariser/train_content')

# Adding the features of the data 



# Creating a model description 

def _info(self):
    return datasets.DatasetInfo(
        description=
        "Training data for annual report summarisation",
        features=datasets.Features(
            {
                "id": datasets.Value("string"),
                "document": datasets.Value("string"),
                "summary": datasets.Value("string"),
                "question": datasets.Value("string")
            }
        ),
        supervised_keys=None,
        homepage="https://huggingface.co/datasets/OdhranR/report_summariser",
        citation="",
    )

# Create a dictionary of URLs in the loading script that point to the original SQuAD data files:

_URL = "report_summariser/train_content"
_URLS = {
    "train": _URL
}

# Defining the train, test and validation subsets of the model

def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
    urls_to_download = self._URLS
    downloaded_files = dl_manager.download_and_extract(urls_to_download)

    return [
        datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
        datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
    ]
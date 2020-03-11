import argparse
import logging
from nltk import word_tokenize
import numpy as np
import os
import pandas as pd
from pathlib import Path
import shutil
import re
from typing import Dict, List, Optional, Tuple
import urllib
import xmltodict
import zipfile

### texts_to_csv logging handler ###

logging.basicConfig(level=logging.INFO, filename="texts_to_csv.log", filemode="w")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s",
                              datefmt='%H:%M')
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)


def get_file_list(path: str) -> List[str]:
    """ Returns a list with files of a given directory. """
    return [file.stem for file in Path(path).glob("**/*.txt") if file.is_file()]

def hasNumbers(inputString: str) -> bool:
    """ Checks if a string has numbers. """
    return any(char.isdigit() for char in inputString)

def get_metadata(filename: str, file: str) -> List:
    """ Splits a string into metadata informations."""
    author = ""
    title = ""
    year = ""

    filename_split = filename.split("-", 1)
    author = filename_split[0].replace("_", " ")[:-1]
    
    # filename_elements = re.findall(r"\w+", "".join(filename_split[1]))
    filename_elements = re.findall(r"\w+(?:-\w+)+|\w+", "".join(filename_split[1]))
    
    if len(filename_elements) > 2:
        if hasNumbers(filename_elements[-1]):
            year = filename_elements[-1]
            joined_title = "".join(filename_elements[:-1])
            title = joined_title.replace("_", " ")[1:-1]
        else:
            year = "0"
            joined_title = "".join(filename_elements)
            title = joined_title.replace("_", " ")[1:-1]
    elif len(filename_elements) == 2:
        if hasNumbers(filename_elements[1]):
            year = filename_elements[1]
            title = filename_elements[0].replace("_", " ")[1:-1]
        else:
            year = "0"
            joined_title = "".join(filename_elements)
            title = joined_title.replace("_", " ")[1:-1]
    elif len(filename_elements) == 1:
        if hasNumbers(filename_elements[0]):
            year = filename_elements[0]
            title = "no_title"
        else:
            year = "0"
            title = filename_elements[0].replace("_", " ")[1:-1]
    elif len(filename_elements) == 0:
        year = "0"
        title = "no_title"
        

    factor = (len(author) + len(title) + 4)*3
    metalist = [author, title, year]
    
    # splits a txt-file into two parts by a factor and replaces informations 
    # about the author, title and year 
    file_p1 = file[:factor]
    file_p2 = file[factor:]
    
    for entry in metalist:
        if entry in file_p1:
            file_p1 = file_p1.replace(entry, "")

    file = file_p1 + file_p2
    file = file.replace("━", "") #replace stroke
    
    tok_text = word_tokenize(file)
    textlength = len(tok_text)
    text = " ".join(tok_text)
    return metalist + [textlength, text]

def prose_to_df(path: str,
                used_dataset: Optional[str] = "corpus-of-german-fiction-txt",
                zip_file: Optional[str] = "CorpusofGermanLanguageFiction.zip",
                keep_unzipped: Optional[bool] = False) -> pd.DataFrame:
    """ Takes a path to a zipfile of prose text files and 
        stores the metadata and the corresponding text into a
        DataFrame.
    """

    logging.info(f"Extracting zipfile.")
    df = None

    zip_path = os.path.join(path, zip_file)

    tmp = {}

    with zipfile.ZipFile(zip_path) as file:
        file.extractall(path=path)

    
    dataset_path = os.path.join(path, f"Corpus of German-Language Fiction/{used_dataset}")
    file_list = get_file_list(dataset_path) 
    
    
    logging.info(f"Parsing texts from '{used_dataset}'.")

    # pare file_list and add meta data with text to dict
    for c, filename in enumerate(file_list):

        file_dir = dataset_path + "/" + filename + ".txt"
        with open(file_dir, encoding="utf-8") as f:
            tmp_file = f.read()
            tmp[filename] = get_metadata(filename, tmp_file)

    logging.info("Creating the DataFrame.")
    # dict to dataframe
    df = pd.DataFrame.from_dict(tmp, orient="index").reset_index()
    df.columns = ["filename", "author", "title", 
                  "year", "textlength", "text"]
    
    if not keep_unzipped:
        logging.info(f"Unzipped files will be deleted. `keep_unzipped = True` prevents this.")
        shutil.rmtree('Corpus of German-Language Fiction', ignore_errors=True)
    
    return df



def speeches_to_df(path: str, 
                   used_dataset: Optional[str] = "Bundesregierung.xml",
                   zip_file: Optional[str] = "German-Political-Speeches-Corpus.zip") -> pd.DataFrame:
    """ Takes a path to the Zipfile 'German-Political-Speeches-Corpus.zip' and 
        returns a DataFrame. Only the XML-file 'Bundesregierung.xml' will be used.


        INFO: The code was adopted in a modified form 
        from the following website: https://www.timmer-net.de/2019/03/24/nlp_basics/
    """
    logging.info(f"Extracting speeches from '{used_dataset}'.")
    df = None

    zip_path = os.path.join(path, zip_file)

    with zipfile.ZipFile(zip_path) as file:
        file.extractall(used_dataset, path=path)
        
    xml_path = os.path.join(path, used_dataset)
    with open(xml_path, mode="rb") as file:
        xml_document = xmltodict.parse(file)
        nodes = xml_document['collection']['text']
        df = pd.DataFrame({'speaker' : [t['@person'] for t in nodes],
                           'title' : [t['@titel'] for t in nodes],
                           'speech' : [t['rohtext'] for t in nodes]})

    return df



def main():

    # TODO: evtl. mehr corpora hinzufügen
    if args.corpus_name == "prose":
        df = prose_to_df(args.path)
        logging.info(f"Writing csv-file to corpora/")
        df.to_csv("corpora/german_prose.csv", index=False)
    elif args.corpus_name == "speeches":
        df = speeches_to_df(args.path)
        logging.info(f"Writing csv-file to corpora/")
        df.to_csv("corpora/german_speeches.csv", index=False)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog="texts_to_csv", description="Saves text corpora in csv files.")
    parser.add_argument("path", type=str, help="Path to the directories.")
    #TODO: help ergänzen
    parser.add_argument("--corpus_name", "-cn", type=str, default="prose", help="Indicates the corpus type. Default is 'prose'. Other value are 'speeches'.")
    args = parser.parse_args()

    main()
    
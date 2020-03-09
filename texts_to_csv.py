import argparse
import logging
from nltk import word_tokenize
import numpy as np
import os
import pandas as pd
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple
import urllib
import xmltodict
import zipfile


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

def speeches_to_df(path: str, 
                   zip_file: Optional[str] = "German-Political-Speeches-Corpus.zip",
                   remote_dataset: Optional[str] = "Bundesregierung.xml") -> str:
    """ INFO: The code was adopted in a modified form 
        from the following website: https://www.timmer-net.de/2019/03/24/nlp_basics/
    """
    logging.info("Writing speeches to DataFrame.")
    df = None

    zip_path = os.path.join(path, zip_file)

    with zipfile.ZipFile(zip_path) as file:
        file.extract(remote_dataset, path=path)
        
    xml_path = os.path.join(path, remote_dataset)
    with open(xml_path, mode="rb") as file:
        xml_document = xmltodict.parse(file)
        nodes = xml_document['collection']['text']
        df = pd.DataFrame({'author' : [t['@person'] for t in nodes],
                            'title' : [t['@titel'] for t in nodes],
                            'text' : [t['rohtext'] for t in nodes]})

    logging.info("Finished writing speeches to DataFrame.")
    return df

def texts_to_df(path: str) -> str:
    """ Takes a path to a directory of text files and saves
        the metadata and the corresponding text into a
        DataFrame.
    """
    d = {}
    file_list = get_file_list(path)

    # pare file_list and add meta data with text to dict
    for c, filename in enumerate(file_list):
        logging.info(f"Text {c+1} von {len(file_list)}.")

        file_dir = path + "/" + filename + ".txt"
        with open(file_dir, encoding="utf-8") as f:
            tmp_file = f.read()
            d[filename] = get_metadata(filename, tmp_file)

    # dict to dataframe
    df = pd.DataFrame.from_dict(d, orient="index").reset_index()
    df.columns = ["filename", "author", "title", 
                  "year", "textlength", "text"]
    return df

def main():
    # TODO: evtl. mehr corpora hinzufügen
    if args.corpus_name == "prose":
        df = texts_to_df(args.path)
        df.to_csv("../corpora/corpus.csv", index=False)
    elif args.corpus_name == "speeches":
        df = speeches_to_df(args.path)
        df.to_csv("../corpora/speeches_corpus.csv", index=False)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog="texts_to_csv", description="Saves text corpora in csv files.")
    parser.add_argument("path", type=str, help="Path to the directories.")
    #TODO: help ergänzen
    parser.add_argument("--corpus_name", "-cn", type=str, default="prose", help="Indicates the corpus type. Default is 'prose'. Other value are 'speeches'.")
    args = parser.parse_args()

    main()
    
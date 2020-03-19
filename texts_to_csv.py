import argparse
import json
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


def clear_string(s: str,
                 replacement: str) -> str:
    """ Cleans a string (no linebreaks, no unnecessary space) 
        and replaces empty strings or NoneType-Objects.
    """

    if s == None: 
        s = replacement
    else:
        s = " ".join(s.split())
        if s == None or s == "":
            s = replacement

    return s

def compute_textlength(df: pd.DataFrame,
                       columnname: Optional[str] = "textlength",
                       textcolumn: Optional[str] = "text") -> pd.DataFrame:
    """ Add a column with the textlength of a text column
        of a DataFrame.
    """

    df[columnname] = df[textcolumn].apply(lambda x: len(word_tokenize(x)))

    return df

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


def poems_to_df(path: str,
                used_dataset: Optional[str] = "deutsches.lyrik.korpus.v3.noduplicates.json"):
    """ Takes a path to a poem jsonfile and stores the
        title, author and text into a DataFrame.
    """
    logging.info(f"Extracting json file contents.")
    df = None

    json_path = os.path.join(path, used_dataset)

    tmp = {}


    with open(json_path) as jsonfile:
        data = json.load(jsonfile)

        for k, v in data.items():
            poet = v["author"]
            title = v["title"]
            year = v["year"]
            poem = " ".join(v["lines"])


            title = clear_string(title, "UNTITLED")
            poet = clear_string(poet, "N.U.")
            year = clear_string(str(year), "0")
            year = int(year)
            poem = clear_string(poem, "NO CONTENT")
                        

            filename = poet + "_" + title + "_" + str(year)

            if filename not in tmp:
                tmp[filename] = {"poet" : poet,
                                 "title" : title,
                                 "year" : year,
                                 "poem": poem}
            else:
                tmp[filename]["poem"] += poem

    tmp2 = {}
    for k, v in tmp.items():
        tmp2[k] = [v["poet"],
                   v["title"],
                   v["year"],
                   v["poem"],
                   len(word_tokenize(v["poem"]))]


    logging.info("Creating the DataFrame.")
    # dict to dataframe
    df = pd.DataFrame.from_dict(tmp2, orient="index").reset_index()
    df.columns = ["filename", "poet", "title", "year", "poem", "poemlength"]  


    logging.info(f"Remove poets with less than 6 poems.")
    df = df.groupby("poet").filter(lambda x: len(x) > 5)

    logging.info(f"Remove poet with no name (= 'N. N.,').")
    df = df[df["poet"] != 'N. N.,']

    logging.info(f"Remove empty poems.")
    df = df[df["poem"] != 'NO CONTENT']

    return df  


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
    
    mean = np.mean(df["textlength"])
    logging.info(f"Remove works with less words than the mean (= {mean}).")
    df = df[df["textlength"] > mean] 

    logging.info(f"Remove authors with less than 6 works.")
    df = df.groupby("author").filter(lambda x: len(x) > 5)   

    if not keep_unzipped:
        logging.info(f"Unzipped files will be deleted. `keep_unzipped = True` prevents this.")
        shutil.rmtree('Corpus of German-Language Fiction', ignore_errors=True)
    
    return df



def speeches_to_df(path: str, 
                   used_dataset: Optional[str] = "Bundesregierung.xml",
                   zip_file: Optional[str] = "German-Political-Speeches-Corpus.zip",
                   keep_unzipped: Optional[bool] = False) -> pd.DataFrame:
    """ Takes a path to the Zipfile 'German-Political-Speeches-Corpus.zip' and 
        returns a DataFrame. Only the XML-file 'Bundesregierung.xml' will be used.


        INFO: The code was adopted in a modified form 
        from the following website: https://www.timmer-net.de/2019/03/24/nlp_basics/
    """
    logging.info(f"Extracting speeches from '{used_dataset}'.")
    df = None

    zip_path = os.path.join(path, zip_file)
    output_path = os.path.join(path, zip_file[:-4])

    with zipfile.ZipFile(zip_path) as file:
        file.extractall(path=output_path)
        
    xml_path = os.path.join(output_path, used_dataset)
    with open(xml_path, mode="rb") as file:
        xml_document = xmltodict.parse(file)
        nodes = xml_document['collection']['text']
        df = pd.DataFrame({'speaker' : [t['@person'] for t in nodes],
                           'title' : [t['@titel'] for t in nodes],
                           'speech' : [t['rohtext'] for t in nodes],
                           'speechlength': [len(word_tokenize(t['rohtext'])) for t in nodes]})


    if not keep_unzipped:
        logging.info(f"Unzipped files will be deleted. `keep_unzipped = True` prevents this.")
        shutil.rmtree(zip_file[:-4], ignore_errors=True)

    return df


def main():

    if args.corpus_name == "prose":
        df = prose_to_df(args.path)
        logging.info(f"Writing csv-file to corpora/")
        df.to_csv("corpora/german_prose.csv", index=False)
    elif args.corpus_name == "speeches":
        df = speeches_to_df(args.path)
        logging.info(f"Writing csv-file to corpora/")
        df.to_csv("corpora/german_speeches.csv", index=False)
    elif args.corpus_name == "poems":
        df = poems_to_df(args.path)
        logging.info(f"Writing csv-file to corpora/")
        df.to_csv("corpora/german_poems.csv", index=False)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog="texts_to_csv", description="Saves text corpora in csv files.")
    parser.add_argument("path", type=str, help="Path to the directories.")
    parser.add_argument("--corpus_name", "-cn", type=str, default="prose", help="Indicates the corpus type. Default is 'prose'. Other value are 'speeches' and 'poems'.")
    args = parser.parse_args()

    main()
    
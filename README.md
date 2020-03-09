# german-corpora
Compilation of several german corpora as csv-files for text classification. 


## Note

I'm not the author of most of the corpora. The authors of the respective original corpora are listed under section **Corpora sources**. Changes to the original corpora are listed in the column "changes". The corpora were converted to csv files using the "texts_to_csv.py" script. Instructions for using the script can be found in the **Usage** section.

## Corpora sources

| corpus | original name | author(s) | source | changes |
| --- |---| ---| --- | --- |
| prose | Corpus of German-Language Fiction | Frank Fischer, Jannik Strötgen | [Link](https://figshare.com/articles/Corpus_of_German-Language_Fiction_txt_/4524680/1) | - |
| speeches | German Political Speeches Corpus | Adrien Barbaresi | [Link](https://adrien.barbaresi.eu/corpora/speeches/#data) | - |
| wikipedia | wikicorpus | Jan Paulus | [Link](https://github.com/realjanpaulus/german_text_classification_nlp) | - |

## Structure of the available csv-files

| name | class column name | text column name |
| --- | --- | --- |
| prose | author | text |
| speeches | speaker| speech |
| ... | ... | ... |

## Usage

```

$ python texts_to_csv.py -h
usage: texts_to_csv [-h] [--corpus_name CORPUS_NAME] path

Saves text corpora in csv files.

positional arguments:
  path                  Path to the directories.

optional arguments:
  -h, --help            show this help message and exit
  --corpus_name CORPUS_NAME, -cn CORPUS_NAME 
                        Indicates the corpus type. Default is 'prose'. Other value are
                        'speeches'.

```

### Requirements

Required: Python 3.6+

TODO: requirements.txt / Pipfile


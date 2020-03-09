# german-corpora
Compilation of several german corpora as csv-files for text classification. 


## Note

I'm not the author of most of the corpora. The authors of the respective original corpora are listed under section **Corpora sources**. Changes to the original corpora are listed in the column "changes". The corpora were converted to csv files using the "texts_to_csv.py" script. Instructions for using the script can be found in the **Usage** section.

## Corpora sources

| corpus | original name | author(s) | source | changes |
| --- |---| ---| --- | --- |
| german_prose | Corpus of German-Language Fiction | Frank Fischer, Jannik Strötgen | [Link](https://figshare.com/articles/Corpus_of_German-Language_Fiction_txt_/4524680/1) | - |
| german_speeches | German Political Speeches Corpus | Adrien Barbaresi | [Link](https://adrien.barbaresi.eu/corpora/speeches/#data) | Only speeches from  the file "Bundesregierung.xml" were read in. |
| german_wiki | wikicorpus_v2 | Jan Paulus | [Link](https://github.com/realjanpaulus/german_text_classification_nlp) | - |
| german_wiki_small | smallwikicorpus_v2 | Jan Paulus | [Link](https://github.com/realjanpaulus/german_text_classification_nlp) | - |

## Structure of the available csv-files

| name | class column name | text column name |
| --- | --- | --- |
| *german_prose* | author | text |
| *german_speeches* | speaker| speech |
| *german_wiki* | category | text |
| *german_wiki_small* | category | text |

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

### Building your own corpus variation

The following table provides information that can be used to create your own corpus variations.

**Example**: 
* Download the required file `German-Political-Speeches-Corpus.zip` from the corresponding [website](https://adrien.barbaresi.eu/corpora/speeches/#data). 
* Call the specified function `speeches_to_csv()` from `texts_to_csv.py`.
* Perform the specified change, indicated in the `change` column.

| corpus | required files| function | change |
| --- | --- | --- | --- |
| speeches | `German-Political-Speeches-Corpus.zip` (should be in the same folder as `texts_to_csv.py` | `speeches_to_csv(`<br> `path: str,` <br> `remote_dataset: Optional[str] = "Bundesregierung.xml"`<br>`) -> pd.DataFrame` | set `remote_dateset` to a different XML-file within the XML-file (*Watch out*: It may be necessary to specify other XML tags in the source code.) |
| ... | ... | ... | ... |

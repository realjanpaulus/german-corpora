# german-corpora
Compilation of several german corpora as csv-files for text classification. 


## Note

I'm not the author of most of the corpora. The authors of the respective original corpora are listed under section **Corpora sources**. Changes to the original corpora are listed in the column "changes". The corpora were converted to csv files using the "texts_to_csv.py" script. Instructions for using the script can be found in the **Usage** section.

## Corpora sources


| corpus | original name | author(s) | content | source | license | changes |
| --- | --- | --- | --- | --- | --- | --- |
| german_news | 10kGNAD | Timo Block | 10273 german language news articles, divided into 9 categories | [Link](https://tblock.github.io/10kGNAD/) | CC BY-NC-SA 4.0 | Replaced semicolon delimiter with comma delimiter. |
| german_prose | Corpus of German-Language Fiction | Frank Fischer, Jannik Strötgen | 2735 german prose works from 548 different german authors. |[Link](https://figshare.com/articles/Corpus_of_German-Language_Fiction_txt_/4524680/1) | CC BY 4.0 | Only prose texts from the folder 'corpus-of-german-fiction-txt' where used i.e. only texts from german authors. |
| german_speeches | German Political Speeches Corpus | Adrien Barbaresi | 2983 speeches from 46 different german speakers. ||[Link](https://adrien.barbaresi.eu/corpora/speeches/#data) | CC BY-SA 4.0 | Only speeches from the file "Bundesregierung.xml" were used. |
| german_wiki | wikicorpus_v2 | Jan Paulus | 6000 tokenized wikipedia articles, divided into 30 different categories. | [Link](https://github.com/realjanpaulus/german_text_classification_nlp) | - | Deleted "id" and "Unammed: 0" column. |
| german_wiki_small | smallwikicorpus_v2 | Jan Paulus | 440 tokenized wikipedia articles, divided into 10 different categories. | [Link](https://github.com/realjanpaulus/german_text_classification_nlp) | - | Deleted "id" and "Unammed: 0" column. |

## Structure of the available csv-files

| name | class column name | text column name |
| --- | --- | --- |
| *german_news* | label | text |
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
| german_speeches | `German-Political-Speeches-Corpus.zip` (should be in the same folder as `texts_to_csv.py` | `speeches_to_csv(`<br> `path: str,` <br> `remote_dataset: Optional[str] = "Bundesregierung.xml"`<br>`) -> pd.DataFrame` | set `remote_dateset` to a different XML-file within the XML-file (*Watch out*: It may be necessary to specify other XML tags in the source code.) |
| german_wiki | see [Wikipedia-building-tutorial (only in german)](https://github.com/realjanpaulus/german_text_classification_nlp/blob/master/tutorials/Zusatzkapitel%20-%20Wie%20baue%20ich%20mein%20eigenes%20Wikipediakorpus%3F.ipynb) | - | - |

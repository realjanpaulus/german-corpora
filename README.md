# german-corpora
Compilation of several german corpora as csv-files. Priority use is intended for text classification.


## Note

I'm not the author of most of the corpora. The authors of the respective original corpora are listed under section **Corpora sources**. Changes to the original corpora are listed in the column "changes". The corpora, which were not previously in csv file format, were converted to csv files using the "texts_to_csv.py" script. Instructions for using the script can be found in the **Getting started** section.

## Corpora sources

Every corpus csv file contains the string "german_" before their name (e.g. `german_news.csv`).

| corpus | original name  | author(s) | content | changes |
| --- | --- | --- | --- | --- |
| news |  [10kGNAD](https://tblock.github.io/10kGNAD/) (**License**: CC BY-NC-SA 4.0) | Timo Block | 10273 german language news articles, divided into 9 categories. | Replaced semicolon delimiter with comma delimiter. Added textlength column.|
| poems | [DLK_v3](https://github.com/tnhaider/DLK) | Thomas Haider, Steffen Eger | 30731 poems in German language by 197 different german and non-german poets. | The poems were composed from the different verses. These are <u>not</u> sorted. Poets with less than 6 poems, empty poems and poems without a specific author (= 'N. N.') were removed from the corpus. Poems without titles were titled with "UNTITLED". Poem ids were removed. Added textlength column. |
| prose | [Corpus of German-Language Fiction](https://figshare.com/articles/Corpus_of_German-Language_Fiction_txt_/4524680/1) (**License**: CC BY 4.0)| Frank Fischer, Jannik Strötgen | 492 german prose works from 50 different german authors. | Only prose texts from the folder 'corpus-of-german-fiction-txt' where used i.e. only texts from german authors. Due to Githhubs file size limitations, authors with less than 6 works were removed from the corpus (the original corpus contained 2735 german prose works from 549 different german authors). In addition, texts with a length less than the mean of all texts and most of the meta-information at the beginning of each work has been removed. Added textlength column.|
| speeches | [German Political Speeches Corpus](https://adrien.barbaresi.eu/corpora/speeches/#data) (**License**: CC BY-SA 4.0) | Adrien Barbaresi | 2917 speeches from 13 different german speakers. | Only speeches from the file "Bundesregierung.xml" were used. Speakers with less than 6 speeches and the speaker "k.A." were removed. Added textlength column.|
| wiki | [wikicorpus_v2](https://github.com/realjanpaulus/german_text_classification_nlp) | Jan Paulus | 6000 tokenized wikipedia articles, divided into 30 different categories. | Deleted "id" and "Unnamed: 0" column. Added textlength column.|
| wiki_small | [small wikicorpus_v2](https://github.com/realjanpaulus/german_text_classification_nlp) | Jan Paulus | 440 tokenized wikipedia articles, divided into 10 different categories. | Deleted "id" and "Unammed: 0" column. Added textlength column.|

## Structure of the available csv-files

| name | class column name | text column name |
| --- | --- | --- |
| *german_news* | label | text |
| *german_poems* | poet | poem |
| *german_prose* | author | text |
| *german_speeches* | speaker| speech |
| *german_wiki* | category | text |
| *german_wiki_small* | category | text |



## Installation

Required: Python 3.6+

`$ pip install -r requirements.txt`


### Pipenv

```
$ pipenv install

$ pipenv shell
```

## Getting started

### `texts_to_csv.py` script

```

$ python texts_to_csv.py -h
usage: texts_to_csv [-h] [--corpus_name CORPUS_NAME] path

Saves text corpora in csv files.

positional arguments:
  path                  Path to the directories.

optional arguments:
  -h, --help            show this help message and exit
  --corpus_name CORPUS_NAME, -cn CORPUS_NAME 
                        Indicates the corpus type. Default is 'prose'. Other value are 'speeches' and 'poems'.

```


### Building your own corpus variation

The following table provides information that can be used to create your own corpus variations.

**Example**: 
* Download the required file `German-Political-Speeches-Corpus.zip` from the corresponding [website](https://adrien.barbaresi.eu/corpora/speeches/#data). 
* Call the specified function `speeches_to_csv()` from `texts_to_csv.py`.
* Perform the specified change, indicated in the `change` column.

| corpus | required files | change |
| --- | --- | --- | 
| news | see [One Million Posts Corpus](https://ofai.github.io/million-post-corpus/) from which 10kGNAD is extracted. | - |
| poems | [Github DLK](https://github.com/tnhaider/DLK) | use different corpus json file as `used_dataset` argument for the function `poems_to_df()`. |
| speeches | `German-Political-Speeches-Corpus.zip` (should be in the same folder as `texts_to_csv.py` | set `remote_dateset` to a different XML-file within the XML-file (*Watch out*: It may be necessary to specify other XML tags in the source code.) |
| wiki | see [Wikipedia-building-tutorial (only in german)](https://github.com/realjanpaulus/german_text_classification_nlp/blob/master/tutorials/Zusatzkapitel%20-%20Wie%20baue%20ich%20mein%20eigenes%20Wikipediakorpus%3F.ipynb) | - |

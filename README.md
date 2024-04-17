# stemmatology
This repo collects scripts and files for stemmatology experiments
## Stemma Texts
### XML_to_collatex.ipynb
This jupyter notebook requires collatex and graphviz python packages. (Installation Guides:http://interedition.github.io/collatex/pythonport.html  https://www.graphviz.org/download/ )

The scripts reads an input ".xml" file with text transcriptions.
It then does the following:
1. parse .xml, clean up text and save plaintext into .txt files
2. starts a collatex collation and imports each .txt file as a witness.
3. outputs the collation results as .csv
The .csv can the by transformed into nexus files using https://github.com/jorisvanzundert/cx2tree/tree/main

### Nexus Files
Nexus files for experiments in PAUP and splitstree


## Stemma Illustrations
tbd
tribes spreadsheet: https://docs.google.com/spreadsheets/d/1b7fyLaNLEgHSAxTDo9vZKiGJNnVajQmd14N3-CaFiEU/edit?usp=sharing

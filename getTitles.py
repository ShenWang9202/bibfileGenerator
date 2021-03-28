import bibtexparser
import re
import os
from os import path
if path.exists('mytitles.txt'):
    os.remove('mytitles.txt')
with open('MyCollection.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

with open("mytitles.txt","a") as file1:
    for entry in bib_database.entries:
        title = entry['title']
        title = title.replace('{','')
        title = title.replace('}','')
        print(title)
        file1.write('%s\n' % title)


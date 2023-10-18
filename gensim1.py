import logging
from pathlib import Path
from bs4 import BeautifulSoup
import codecs
from gensim import corpora
from pprint import pprint  # pretty-printer
from collections import defaultdict
from gensim import corpora
import re

pattern_remove_quotes = re.compile('["\']')
pattern_make_type_val_to_one_word = re.compile("([a-z]+)=([a-z]+)")
pattern_leave_alpha_numeric = re.compile('[\W]+', re.UNICODE)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class MyCorpus_file_iter(object):
    def __init__(self,dir_path):
        self.dir_path = dir_path

    def __iter__(self):
        pathlist = Path(self.dir_path).glob('**/*.htm*')
        for path in pathlist:
            f = codecs.open(path, encoding='utf-8')
            # print("reading "+ str(path))
            html_str = f.read()
            doc = BeautifulSoup(html_str, 'html.parser')
            forms = doc.findAll('form')
            for form in forms:

                form = str(form).lower().replace('"', "'")
                form = re.sub(pattern_remove_quotes, '', form)
                form = re.sub(pattern_make_type_val_to_one_word,r'\1_\2', form)
                form = re.sub(pattern_leave_alpha_numeric,' ', form)
                form = form.split()
                form = [w.lower() for w in form if not w.isdigit()]
                yield form


def create_forms_iter():
    return MyCorpus_file_iter('C:/Users/hedbn/Documents/site_corpus/')  # doesn't load the corpus into memory!

dictionary = corpora.Dictionary(create_forms_iter())

dictionary.filter_extremes(no_below=5, no_above=0.8, keep_n=100000, keep_tokens=['type_password'])

corpus = [dictionary.doc2bow(form) for form in create_forms_iter()]

for form_bow in corpus:
    for word in form_bow:
        print('{}:{}, '.format(dictionary[word[0]],word[1]), end="")

    print('')


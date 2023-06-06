import os

import shutil

home = os.getcwd()
corpus_folder = 'corpus'
texts_folder = 'unity_code'

with open(f'{home}/{corpus_folder}/mergers/{texts_folder}.txt','wb') as destination_file:
    for filename in os.listdir(f'{home}/{corpus_folder}/{texts_folder}'):
        with open(f'{home}/{corpus_folder}/{texts_folder}/{filename}','rb') as current_file:
            shutil.copyfileobj(current_file, destination_file)
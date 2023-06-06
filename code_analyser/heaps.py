import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats

root = os.getcwd()
corpus_path = 'corpus/mergers'
figure_path = 'figures'
textname = 'songs'

with open(f'{root}/{corpus_path}/{textname}.txt', 'r') as file:
    lines = file.read()

text = lines.split(' ')

lengths = []
vocabs = []

step = 100

for i in range(100, len(text), step):
    lengths.append(i)
    vocabs.append(len(set(text[:i])))
    

print(f'Length of text in words is: {len(text)}')
print(f'Vocabulary size is: {len(set(text))}')

slope, intercept, r, p, se = stats.linregress(x=np.log(lengths[start:]), y=np.log(vocabs[start:]))

print(f'slope is {slope:.4}')
print(f"Pearson's correlation is {r:.4}")

fig, ax = plt.subplots(dpi=300)

ax.set(xscale='log', yscale='log', xlabel=r'$L$', ylabel=r'$V$')

ax.scatter(lengths[::], vocabs[::], facecolor='white', edgecolor='black', label='data')
ax.plot(lengths, np.e**intercept * lengths**slope, '--', color='red', label=f'Heaps')

ax.legend()

plt.show()

plt.savefig(f'{root}/{figure_path}/{textname}-heaps.png')
import os

import pandas as pd
import numpy as np
from scipy import stats

import matplotlib.pyplot as plt

from collections import Counter

directory = os.getcwd()

folder = 'processed'
filename = 'EditorGUI'

with open(f'{directory}/{folder}/{filename}.txt', 'r') as file:
    lines = file.read()
    

text = lines.split(' ')

unique = Counter(text)

vocab = pd.DataFrame.from_dict(unique, orient='index').reset_index()
vocab = vocab.rename(columns={"index": "word", 0: "freq"})
vocab = vocab.sort_values(by='freq', ascending=False, ignore_index=True)
vocab.index = vocab.index + 1
vocab['norm_freq'] = vocab['freq'] / vocab['freq'].sum()

################################## Перший закон Ціпфа ######################################

start = 50
end = 5000

slope, intercept, r, p, se = stats.linregress(x=np.log(vocab.index[start:end]), y=np.log(vocab['freq'][start:end]))

print("---------- ZIPF'S LAW --------------")
print(f"slope is {slope:.4}")
print(f"Pearson's correlation is {r:.4}")

fig, ax = plt.subplots(dpi=300)

ax.set(xscale='log', yscale='log', xlabel=r'$r$', ylabel=r'$f(r)$')

ax.scatter(vocab.index, vocab['norm_freq'], edgecolor='black', facecolor='white', label='data')
ax.plot(vocab.index.to_numpy(), np.e**intercept * vocab.index.to_numpy()**slope, '--', color='red', label='Zipf')

ax.legend()

plt.savefig(f'{directory}/figures/{filename}_zipfs-law.png')

################################# Другий закон Ціпфа #################################

probs, bins = np.histogram(vocab['norm_freq'], bins='fd')

pdf = pd.DataFrame()
pdf['bins'] = bins[:-1]
pdf['probs'] = probs / len(vocab['norm_freq'])

pdf = pdf[pdf['probs'] != 0].reset_index(drop=True)
pdf.index = pdf.index + 1

start_rank = 5
end_rank = 250

slope, intercept, r, p, se = stats.linregress(x=np.log(pdf['bins'][start_rank:end_rank]), y=np.log(pdf['probs'][start_rank:end_rank]))

print("------------ ZIPF'S DISTRIBUTION ---------------")
print(f"slope is {slope:.4}")
print(f"Pearson's correlation is {r:.4}")

fig, ax = plt.subplots(dpi=300)

ax.set(xscale='log', yscale='log', xlabel=r'$f$', ylabel=r'$p(f)$')

ax.scatter(pdf['bins'], pdf['probs'], edgecolor='black', facecolor='white')
ax.plot(pdf['bins'][:end_rank].to_numpy(), np.e**intercept * pdf['bins'][:end_rank].to_numpy()**slope, '--', color='red', label='Zipf')

ax.legend()

plt.savefig(f'{directory}/figures/{filename}_pdf.png')

########################## Закон Парето #######################################

pdf['cdf'] = np.cumsum(pdf['probs'])
pdf['ccdf'] = 1 - pdf['cdf']

slope, intercept, r, p, se = stats.linregress(x=np.log(pdf['bins'][5:end_rank]), y=np.log(pdf['ccdf'][5:end_rank]))

print("------------ PARETO'S LAW --------------")
print(f"slope is {slope:.4}")
print(f"Pearson's correlation is {r:.4}")

fig, ax = plt.subplots(dpi=300)

ax.set(xscale='log', yscale='log', xlabel=r'$f$', ylabel=r'$P(f)$', ylim={1e-5, 2})

ax.scatter(pdf['bins'], pdf['ccdf'], edgecolor='black', facecolor='white')
ax.plot(pdf['bins'].to_numpy(), np.e**intercept * pdf['bins'].to_numpy()**slope, '--', color='red', label='Zipf')

ax.legend()

plt.savefig(f'{directory}/figures/{filename}_ccdf.png')

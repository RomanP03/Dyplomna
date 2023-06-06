import pandas as pd

from scipy import stats
import numpy as np

import os

import matplotlib.pyplot as plt


directory = os.getcwd()
folder = 'processed'

data_inside = {}

for root, dirs, files in os.walk(f'{directory}/{folder}'):
    for file in files:
        filename, extension = os.path.splitext(file)
        if extension == '.txt':
            # print(file)
            vocab_counter = 0
            length_counter = 0
            vocab = []
            with open(f'{root}/{file}', 'r') as f:
                text = f.read().split(' ')
                for word in text:
                    if not word in vocab:
                        vocab.append(word)


            data_inside[file] = (len(text), len(vocab))
            

data = pd.DataFrame.from_dict(data_inside, orient='index').reset_index()
data = data.rename(columns={'index': 'name', 0: 'length', 1: 'vocab_size'})

data = data.sort_values(by=['length'], ignore_index=True)

########################## Корпус ################################################

fig, ax = plt.subplots(dpi=300)

ax.set(xscale='log', yscale='log', xlabel=r'$L$', ylabel=r'$V$')

ax.scatter(data['length'], data['vocab_size'], edgecolor='black', facecolor='white')

# plt.savefig(f'{directory}/figures/unity-corpuse.png')

###################### Аналіз впливу розміру вікна ################################

alpha_1 = []
alpha_2 = []
gamma   = []

windows = [i for i in range(5, 300)]

for window in windows:
    step = window
    ls = data['length'].rolling(window=window, step=step).mean()
    vs = data['vocab_size'].rolling(window=window, step=step).mean()
    dv = data['vocab_size'].rolling(window=window, step=step).std()
    
    slope, intercept, r, p, se = stats.linregress(np.log(ls.dropna()), np.log(vs.dropna()))
    
    alpha_1.append(slope)
    
    slope, intercept, r, p, se = stats.linregress(np.log(ls.dropna()), np.log(dv.dropna()))
    
    alpha_2.append(slope)
    
    slope, intercept, r, p, se = stats.linregress(np.log(vs.dropna()), np.log(dv.dropna()))
    
    gamma.append(slope)
    
########################## Розрахунок для одного розміру вікна #########################

window = 50
step = window

ls = data['length'].rolling(window=window, step=step).mean()
vs = data['vocab_size'].rolling(window=window, step=step).mean()
dv = data['vocab_size'].rolling(window=window, step=step).std()

########################### Визначення символів для підписів ##############################

r_symbol = r'$r = $'
alpha1_symbol = r'$\alpha_1 =$'
alpha2_symbol = r'$\alpha_2 =$'
gamma_symbol = r'$\gamma = $'

############################ Закон Гіпса ######################################

slope, intercept, r, p, se = stats.linregress(np.log(ls.dropna()), np.log(vs.dropna()))

print("------------ HEAPS' LAW ------------------")
print(f"slope is {slope:.4}")
print(f"Pearson's correlation is {r:.4}")

fig, ax = plt.subplots(dpi=300)

ax.set(xscale='log', yscale='log', xlabel=r'$L$', ylabel=r'$V$')

ax.scatter(ls, vs, color='black', label='data')
ax.plot(ls.dropna().tolist(),  np.e**intercept * ls.dropna().to_numpy()**slope, '--', color='red', label='fit')

ax.text(x=70, y=120, s=f'{gamma_symbol}{slope:.3},\n {r_symbol}{r:.3}')

ax.legend()

# plt.savefig(f'{directory}/figures/songs_window50_step50_VL.png')

############################## Скейлінґ флуктуацій #####################################

slope, intercept, r, p, se = stats.linregress(np.log(ls.dropna()), np.log(dv.dropna()))

print("------------ FLUCTUATION SCALING -------------")
print(f"slope is {slope:.4}")
print(f"Pearson's correlation is {r:.4}")

fig, ax = plt.subplots(dpi=300)

ax.set(xscale='log', yscale='log', xlabel=r'$L$', ylabel=r'$\Delta V$')

ax.scatter(ls, dv, color='black', label='data')
ax.plot(ls.dropna().tolist(),  np.e**intercept * ls.dropna().to_numpy()**slope, '--', color='red', label='fit')

ax.text(x=100, y=105, s=f'{alpha1_symbol}{slope:.3},\n {r_symbol}{r:.3}')

ax.legend()

# plt.savefig(f'{directory}/figures/songs_window50_step50_dVL.png')

############################### Закон Тейлора #########################################

slope, intercept, r, p, se = stats.linregress(np.log(vs.dropna()), np.log(dv.dropna()))

print("------------ TAYLOR'S LAW -------------")
print(f"slope is {slope:.4}")
print(f"Pearson's correlation is {r:.4}")

fig, ax = plt.subplots(dpi=300)

ax.set(xscale='log', yscale='log', xlabel=r'$V$', ylabel=r'$\Delta V$')

ax.scatter(vs, dv, color='black', label='data')
ax.plot(vs.dropna().tolist(),  np.e**intercept * vs.dropna().to_numpy()**slope, '--', color='red', label='fit')

ax.text(x=100, y=105, s=f'{alpha2_symbol}{slope:.3},\n {r_symbol}{r:.3}')

ax.legend()

# plt.savefig(f'{directory}/figures/songs_window50_step50_dVV.png')

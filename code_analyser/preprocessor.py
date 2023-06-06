import pandas as pd

import re

import matplotlib.pyplot as plt

import os

def dotsub(lines):
    lines = re.sub('\.\.', ' .. ', lines)
    lines = re.sub('(?<=[a-zA-Z_\?])\.(?=[a-zA-Z_\.])', ' . ', lines)
    return lines

def bracketsub(lines):
    lines = re.sub('{', '{ ', lines)
    lines = re.sub('\(', ' ( ', lines)
    lines = re.sub('\[', ' [ ', lines)
    return lines

def ltsub(lines):
    return re.sub('<[^=-]', ' < ', lines)

def gtsub(lines):
    return re.sub('(?<=[^=])>', ' > ', lines)

def equalsub(lines):
    return re.sub('=[^=>]', '= ', lines)

def pointersub(lines):
    return re.sub('-[^>]', '- ', lines)

def plussub(lines):
    lines = re.sub('\+\+', ' ++ ', lines)
    lines = re.sub('\+[^\+]', ' + ', lines)
    return lines

def minussub(lines):
    lines = re.sub('--', ' -- ', lines)
    lines = re.sub('-[^-]', ' - ', lines)
    return lines

def slashsub(lines):
    lines = re.sub('\*', ' * ', lines)
    lines = re.sub(r'\\', ' \ ', lines)
    return lines

def questsub(lines):
    return re.sub('\?[^\.]', ' ? ', lines)

def spacesub(lines):
    return re.sub('\s+', ' ', lines)

def punctsub(lines):    
    lines = re.sub(':', ' : ', lines)
    lines = re.sub(';', ' ; ', lines)
    lines = re.sub('"', ' " ', lines)
    return lines

def main():
    directory = os.getcwd()

    directories = ['profilereader-main', 'unitychanspringbone', 'unityrenderstreaming', 'anotherthread-game', 'fpssample-game', 'unitycsreference', 'waveshooter-demo']

    # directory_path = directory[7]

    directory_path = 'unitycsreference'
    for file in os.listdir(f'{directory}/source/{directory_path}'):
        filename, _ = os.path.splitext(file)

        with open(f'{directory}/source/{directory_path}/{file}') as f:
            lines = []
            for line in f.readlines():
                if not line.strip().startswith('/'):
                    line = re.sub(r'.*?\/(.*)$', '', line)
                    lines.append(line)

        lines = ' '.join(lines).replace('\n', ' \n ').replace(',', ' ').replace('@', '').replace(')', '').replace('}', '').replace(']', '')

        # рядок про крапку
        lines = dotsub(lines)
        lines = bracketsub(lines)
        
        # про < і не <=
        lines = ltsub(lines)
        
        # про > і не =>
        lines = gtsub(lines)

        # = і не ==
        lines = equalsub(lines)
        
        # ->
        lines = pointersub(lines)
        
        # + і не ++x чи x++
        lines = plussub(lines)

        # -
        lines = minussub(lines)

        # * \
        lines = slashsub(lines)

        # рядок про ? за винятком ?.
        lines = questsub(lines)

        # lines = 
        # замінити кілька пробілів одним
        lines = spacesub(lines)

       # with open(f'{directory}/corpus/unity_code/{filename}.txt', 'w') as f:
       #     f.write(lines)
            
if __name__=='__main__':
    main()

from os import listdir
import collections
import os
import re

NUM_OF_FILES = 6


# Usage Ex: TODO
def main()
  cnt = [0] * NUM_OF_FILES
  step = 0
  dir_list = listdir('../Search_Results')
  for directory in dir_list:
    if os.path.isdir('../Search_Results/' + directory):
      file_list = listdir('../Search_Results/' + directory)

      for file in file_list:
        f = open('../Search_Results/' + directory + '/' + file)
        print(f.name)
        # Result file open
        if f.name.find('MergedFDR.tsv') == -1:
          continue
          
        f.readline()
        for line in f.readlines():
          l = line.split('\t')
          length = check_modification(l[9])
          Q_value = float(l[15])
          charge = int(l[8])

          if length == 11:
            # 11_2_000
            if charge == 2 and Q_value == 0.0:
              cnt[0] += 1
            # 11_2_001
            if charge == 2 and Q_value <= 0.01:
              cnt[1] += 1
            # 11_3_000
            if charge == 3 and Q_value == 0.0:
              cnt[2] += 1
            # 11_3_001
            if charge == 3 and Q_value <= 0.01:
              cnt[3] += 1
            # 11_4_000
            if charge >= 4 and Q_value == 0.0:
              cnt[4] += 1
            # 11_4_001
            if charge >= 4 and Q_value <= 0.01:
              cnt[5] += 1
        step += 1
        print(step)

  f = open('peptide_stats.txt', 'wt', encoding='utf-8')
  for i in range(NUM_OF_FILES):
    f.write(str(cnt[i]) + '\n')
  f.close()


# Only allow modification C+57.021
def check_modification(peptide):
  p = re.compile('[^a-zA-Z]')
  strip_peptide = p.sub('', peptide)
  if peptide == strip_peptide:
    return len(strip_peptide)
  else:
    for i in range(len(peptide)):
      if peptide[i] == '-':
        return False
      if peptide[i] == '+'\
        and peptide[i + 1: i + 7] != '57.021':
        return False
  return len(strip_peptide)

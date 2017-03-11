import collections
from os import listdir
import re

NUM_OF_FILES = 6

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

d = [{}] * NUM_OF_FILES
step = 0

fout = [open('peptide_11_2_000.tsv', 'wt', encoding='utf-8'),
        open('peptide_11_2_001.tsv', 'wt', encoding='utf-8'),
        open('peptide_11_3_000.tsv', 'wt', encoding='utf-8'),
        open('peptide_11_3_001.tsv', 'wt', encoding='utf-8'),
        open('peptide_11_4_000.tsv', 'wt', encoding='utf-8'),
        open('peptide_11_4_001.tsv', 'wt', encoding='utf-8')]

dir_list = listdir('../PeptideSearchResult')
for directory in dir_list:
  file_list = listdir('../PeptideSearchResult/' + directory)
  for file in file_list:
    f = open('../PeptideSearchResult/' + directory + '/' + file)
    f.readline()
    for line in f.readlines():
      l = line.split('\t')
      length = check_modification(l[9])
      Q_value = float(l[15])
      charge = int(l[8])

      if length == 11:
        # 11_2_000
        if charge == 2 and Q_value == 0.0:
          if length in d[0].keys():
            d[0][length] += 1
          else:
            d[0][length] = 1

          fout[0].write(line)

        # 11_2_001
        if charge == 2 and Q_value <= 0.01:
          if length in d[1].keys():
            d[1][length] += 1
          else:
            d[1][length] = 1

          fout[1].write(line)

        # 11_3_000
        if charge == 3 and Q_value == 0.0:
          if length in d[2].keys():
            d[2][length] += 1
          else:
            d[2][length] = 1

          fout[2].write(line)

        # 11_3_001
        if charge == 3 and Q_value <= 0.01:
          if length in d[3].keys():
            d[3][length] += 1
          else:
            d[3][length] = 1

          fout[3].write(line)

        # 11_4_000
        if charge >= 4 and Q_value == 0.0:
          if length in d[4].keys():
            d[4][length] += 1
          else:
            d[4][length] = 1

          fout[4].write(line)

        # 11_4_001
        if charge >= 4 and Q_value <= 0.01:
          if length in d[5].keys():
            d[5][length] += 1
          else:
            d[5][length] = 1

          fout[5].write(line)
    f.close()
    step += 1
    print(step)

for file in fout:
  file.close()

od1 = [collections.OrderedDict(sorted(d1.items())),
       collections.OrderedDict(sorted(d2.items())),
       collections.OrderedDict(sorted(d6.items()))]
       collections.OrderedDict(sorted(d3.items())),
       collections.OrderedDict(sorted(d4.items())),
       collections.OrderedDict(sorted(d5.items())),
cnt_all = [0] * NUM_OF_FILES

for i in range(NUM_OF_FILES):
  for k in d[i].keys():
    cnt_all[i] += d[i][k]

f = open('peptide_stats.txt', 'wt', encoding='utf-8')

for i in range(NUM_OF_FILES):
  f.write(str(od[i]) + '\n')
  f.write(str(cnt_all[i]) + '\n')

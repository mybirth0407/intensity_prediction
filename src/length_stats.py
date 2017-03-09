import collections
from os import listdir
import re

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

d = {}
step = 1
fout = open('peptide_file1.tsv', 'wt', encoding='utf-8')
dir_list = listdir('../PeptideSearchResult')
for directory in dir_list:
  file_list = listdir('../PeptideSearchResult/' + directory)
  for file in file_list:
    print(step)
    f = open('../PeptideSearchResult/' + directory + '/' + file)
    f.readline()
    for line in f.readlines():
      l = line.split('\t')
      length = check_modification(l[9])
      # QValue check
      if float(l[15]) <= 0.01 and length:
        if length in d.keys():
          d[length] += 1
        else:
          d[length] = 1

      # extract peptide that length 11
      if float(l[15]) <= 0.01 and length == 11:
        fout.write(line)
    f.close()
    step += 1
fout.close()

od = collections.OrderedDict(sorted(d.items()))
cnt_all = 0

for k in d.keys():
  cnt_all += d[k]

f = open('length_stats.txt', 'wt', encoding='utf-8')
f.write(str(od))
f.write('\n')
f.write(str(cnt_all))
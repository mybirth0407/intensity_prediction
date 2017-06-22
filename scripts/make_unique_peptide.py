from os import listdir
from os import remove
import csv
import sys
import numpy as np

# sys.argv[1]: old file, sys.argv[2]: new file

f_old = open(sys.argv[1], 'rt', encoding='utf-8')
feature_dict = {}
key_dict = {}

progress = 0
for line in f_old.readlines():
  if progress % 100 == 0:
    print(progress)

  l = line.strip()
  if len(l) < 1:
    continue

  input_vector = l.split()[: 772]
  key = ' '.join(str(x) for x in input_vector)
  output_vector_ = [float(e) for e in l.split()[772: 782]]
  output_vector = np.array(output_vector_).astype('float32')
  if key in feature_dict:
    feature_dict[key] += output_vector
    key_dict[key] += 1
  else:
    feature_dict[key] = output_vector
    key_dict[key] = 1
  progress += 1
f_old.close()

for key in feature_dict:
  feature_dict[key] /= key_dict[key]

f_new = open(sys.argv[2], 'wt', encoding='utf-8')

for key in feature_dict:
  f_new.write(key + ' ')
  for e in feature_dict[key]:
    f_new.write(str(e) + ' ')
  f_new.write('\n')
f_new.close()
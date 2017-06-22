import numpy as np
import sys

# usage: [features file] [write file]

data = np.loadtxt(sys.argv[1], dtype='float64')
features = data[:, 0:772]
# i'th, min, max, zero count
test_list = []


for i in range(772):
  temp = []
  sf = features[:, i]
  temp.append(i)
  temp.append(min(sf))
  temp.append(max(sf))
  temp.append(len(sf) - len(np.nonzero(sf)[0]))
  test_list.append(temp)

f = open(sys.argv[2], 'wt', encoding='utf-8')

f.write(str(len(features))+ '\n')
for t in test_list:
  f.write(str(t) + '\n')
f.close()

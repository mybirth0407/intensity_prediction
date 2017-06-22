import numpy as np
import sys

FEATURE_LEN = 772

# Usage Ex: y_unique.txt y_feat_test.txt
def main(argv):
  data = np.loadtxt(sys.argv[1], dtype='float64')
  features = data[:, 0:FEATURE_LEN]
  # i'th, min, max, zero count
  test_list = []

  for i in range(FEATURE_LEN):
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

if __name__ == '__main__':
  main(sys.argv)
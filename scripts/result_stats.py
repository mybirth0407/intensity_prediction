import sys
import numpy as np
from scipy.spatial.distance import cosine
from sklearn.metrics import mean_squared_error
from math import sqrt


# [result file] [output file]
def main(argv):
  real, pred = file2array(sys.argv[1], ignore_zero=False)

  rmses = np.zeros((10,), dtype='float64')
  variances = np.zeros((10,), dtype='float64')
  cosines = np.zeros((10,), dtype='float64')

  print(pred[:, 0])

  for i in range(10):
    rmses[i] = sqrt(mean_squared_error(real[:, i], pred[:, i]))
    variances[i] = np.var(pred[:, i] - real[:, i], ddof=1)
    cosines[i] = cosine(pred[:, i], real[:, i])

  f = open(argv[2], 'wt', encoding='utf-8')
  f.write('rmses\n')
  f.write(str(rmses) + '\n')
  f.write('variances\n')
  f.write(str(variances) + '\n')
  f.write('cosines\n')
  f.write(str(cosines) + '\n')
  f.close()

def file2array(file, ignore_zero=True):
  f = open(file, 'rt', encoding='utf-8')

  real = []
  pred = []

  for line in f.readlines():
    l = line.split()
    # number. line
    if 1 >= len(l):
      continue

    # ion 1 - 10 slicing
    l = l[2:12]
    # case in last character is ']'
    if ']' == l[-1][-1]:
      l[-1] = l[-1][:-1]

    if 'r' == line[0]:
      real.append(l)
    elif 'p' == line[0]:
      pred.append(l)

  if ignore_zero:
    counter = len(real)
    i = 0

    while i < counter:
      r = [float(e) for e in real[i]]
      p = [float(e) for e in pred[i]]
      if 0 == np.sum(r) or 0 == np.sum(p):
        del real[i]
        del pred[i]
        counter -= 1
        i -= 1
      i += 1

  return np.asarray(real, dtype='float64'), np.asarray(pred, dtype='float64')


if __name__ == '__main__':
  main(sys.argv)
  
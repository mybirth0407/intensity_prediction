import numpy as np
import sys

def count_zero(input_file, result_file, ion_type):
  data = np.loadtxt(input_file, dtype='float32')
  intensities = data[:, -10:]
  zeros = [0] * 10
  non_zeros = [0] * 10

  for i in range(0, 10):
    print(i)
    for e in intensities[:, i]:
      if e == 0:
        zeros[i] += 1
      else:
        non_zeros[i] += 1

  f = open(result_file, 'wt', encoding='utf-8')
  f.write('zeros' + '\n')
  f.write(str(zeros) + '\n')
  f.write('non zeros' + '\n')
  f.write(str(non_zeros) + '\n')
  return zeros, non_zeros

count_zero(sys.argv[1], sys.argv[2], sys.argv[3])

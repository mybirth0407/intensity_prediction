import numpy as np
import sys

# Usage Ex: python ion_check.py y_unique.txt y_check.txt y
def main(argv):
  count_zero(argv[1], argv[2], argv[3])
  

def count_zero(input_file, result_file, ion_type):
  data = np.loadtxt(input_file, dtype='float64')
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

if __name__ == '__main__':
  main(sys.argv)
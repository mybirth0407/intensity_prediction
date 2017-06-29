import matplotlib.pyplot as plt
import sys


def main(argv):
  f = open(argv[1], 'rt', encoding='utf-8')
  n = int(argv[2])
  # train error
  f.readline()
  x = []
  # # of epochs
  for i in range(n):
    x.append(f.readline())

  f.readline()
  # test error
  f.readline()

  y = []
  y.append(f.readline())
  f.close()

  plt.plot(x)
  plt.plot(n, y, 'ro')
  plt.show()

if __name__ == '__main__':
  main(sys.argv)
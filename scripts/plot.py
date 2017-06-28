import matplotlib.pyplot as plt
import sys


def main(argv):
  f = open(argv[1], 'rt', encoding='utf-8')

  # train error
  f.readline()
  x = []
  # # of epochs
  for i in range(5000):
    x.append(f.readline())

  f.readline()
  # test error
  f.readline()

  y = []
  y.append(f.readline())
  f.close()

  plt.plot(x)
  plt.plot(y, 'ro')
  plt.show()

if __name__ == '__main__':
  main(sys.argv)
from os import listdir
from os import remove
import csv
import sys

# Usage Ex: python combine_txt.py HCD all.txt
def main(argv):
  # file already exist, remove that file
  try:
    remove(argv[2])
  except:
    pass

  directory = listdir(argv[1])
  csv_contents = []
  for file in directory:
    if file.find('txt') != -1\
      and file.find('error') == -1\
      and file.find('zeros') == -1:
        f = open(sys.argv[1] + '/' + file, 'rt')

        for line in f.readlines():
          csv_contents.append(line)
        f.close()

  f = open(sys.argv[2], 'wt')
  for content in csv_contents:
    f.write(content)
  f.close()

if __name__ == '__main__':
  main(sys.argv)
from os import listdir
from os import remove
import csv
import sys

remove(sys.argv[2])
directory = listdir(sys.argv[1])
csv_contents = []
for file in directory:
  if file.find('txt') != -1:
    f = open(sys.argv[1] + file, 'rt')

    for line in f.readlines():
      csv_contents.append(line)
    f.close()

f = open(sys.argv[2], 'wt')
for content in csv_contents:
  f.write(content)

f.close()

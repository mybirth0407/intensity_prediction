from os import listdir
import csv
import sys

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

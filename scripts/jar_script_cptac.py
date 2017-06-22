from os import listdir
import os
import sys

# External hard disk location
EXTUSB = '~/media/extusb'

file_list = []
folder_list = []

directory = listdir(sys.argv[1])
for tsv_file in directory:
  index = tsv_file.find('_MSGF_')
  # _MSGF_ is exist
  if index != -1:
    # Remove after _MSGF_
    tsv_file = tsv_file[0: index]
  # File name - _MSGF_Merged.tsv
  file_list.append('./LabelFree_Result_CPTAC/' + tsv_file)

f = open('mgf_location_table.txt')

for line in f.readlines():
  # Last line
  if line == '\r\n':
    continue

  # Remove scratch
  line = line.replace('/scratch', EXTUSB)
  # mzid folder is exist
  index = line.find('/mzid/')
  if index != -1:
    # Remove after mzid
    line = line[0: index]
  folder_list.append(line)
f.close()

ffile = open('file.txt', 'wt', encoding='utf-8')
ffolder = open('folder.txt', 'wt', encoding='utf-8')
ffile.write(str(file_list))
ffolder.write(str(folder_list))
ffile.close()
ffolder.close()

for file in file_list:
  for folder in folder_list:
    # File is a substring of the folder
    # 25 is LabelFree_Result_CPTAC, LabelFree_Result_PRIDE length
    index = folder.find(file[25: ])
    if index != -1:
      print(file[25: ], folder)
      os.system(
        'java -jar MatchedPeakExtractor_revised_nterm.jar -i ' + file
        + '_MSGF_MergedFDR.tsv ' + '-d ' + folder)
      


from os import listdir
import os

# External hard disk location
EXTUSB = '~/media/extusb/Tumor/Search'

directory = listdir('./LabelFree_Result_CPTAC')
file_list = []

folder_list = []

for tsv_file in directory:
  index = tsv_file.find('_MSGF_')
  # _MSGF_ is exist
  if index != -1:
    # Remove after _MSGF_
    tsv_file = tsv_file[0: index]
  # File name - _MSGF_Merged.tsv
  file_list.append('./LabelFree_Result_CPTAC/' + tsv_file)

directory = listdir('./LabelFree_Result_PRIDE')
for tsv_file in directory:
  index = tsv_file.find('_MSGF_')
  # _MSGF_ is exist
  if index != -1:
    # Remove after _MSGF_
    tsv_file = tsv_file[0: index]
  # File name - _MSGF_Merged.tsv
  file_list.append('./LabelFree_Result_PRIDE/' + tsv_file)

f = open('mgf_location_table.txt')

for line in f.readlines():
  # Last line
  if line == '\r\n':
    continue

  # Remove scratch
  line = line.replace('/scratch', '')
  # mzid folder is exist
  index = line.find('/mzid/')
  if index != -1:
    # Remove after mzid
    line = line[0: index]
  line = EXTUSB + line
  folder_list.append(line)
f.close()

# ffile = open('file.txt', 'wt', encoding='utf-8')
# ffolder = open('folder.txt', 'wt', encoding='utf-8')
# ffile.write(str(file_list))
# ffolder.write(str(folder_list))
# ffile.close()
# ffolder.close()

for file in file_list:
  for folder in folder_list:
    # File is a substring of the folder
    index = folder.find(file)
    if index != -1:
      print(file, folder)
      os.system(
        'java -jar MatchedPeakExtractor.jar -i ' + file
        + '_MSGF_MergedFDR.tsv ' + '-d ' + folder)
      






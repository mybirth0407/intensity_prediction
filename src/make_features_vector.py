import peptide
from os import listdir
import re
import peptide
import time

# 0 file 2 scannum 8 charge 9 peptide 15 qvalue
EXTRACTED = '_ExtractedFeature.tsv'

def get_strip_sequence(peptide):
    p = re.compile("[^a-zA-Z]")
    return p.sub('', peptide)

def features_and_intensity(dir_path, charge, length, qvalue, ion_type):
  error = 0
  directory = listdir(dir_path)
  directory.sort()
  step = 0

  for file in directory:
    print(step)
    # If result file, not extracted file
    if file.find('MergedFDR.tsv') != -1:
      # Result file open
      fr = open(dir_path + '/' + file)
      fr.readline()
      results = []

      for line in fr.readlines():
        l = line.split('\t')

          # Charge 2, limit peptide length 11
        if int(l[8]) == charge\
          and len(get_strip_sequence(l[9])) == length\
          and float(l[15]) <= qvalue:

          # SpecFile, scannum, charge, peptide
          results.append((l[0], l[2], l[8], l[9]))
      fr.close()

      extracts = {}
      temp_key = None

      # Extracted file open
      fe = open(dir_path + '/' + file[: file.find('.tsv')] + EXTRACTED)
      for line in fe.readlines():
        if line == '\n':
          temp_key = None
          continue

        l = line.split('\t')

        try:
          # Length 11
          if line[0] == '>'\
            and len(get_strip_sequence(l[2])) == length:
            # create dict key
            extracts[l[0][1: ] + l[1]] = [0] * (length - 1)
            temp_key = l[0][1: ] + l[1]
          elif line[0] == ion_type and temp_key != None:
            # b ions
            extracts[temp_key][int(l[0][1: ]) - 1] = float(l[2])
        except:
          print(fe.name)
          print(l)
          error += 1

      feat_inten_file_name = file[: file.find('MSGF')]
      ffi = open('../data/' + feat_inten_file_name
               + str(length) + '_'
               + str(charge) + '_'
               + str(qvalue) + '.txt',
                 'wt', encoding='utf-8')
      for result in results:
        # Write each file separately
        # 2: charge, 3: peptide
        p = peptide.Peptide(result[3], result[2])
        feat = p.get_features()
        # 0: specfile, 2: peptide, 3: qvalue
        key = result[0] + result[1]
        if key in extracts.keys():
          intensity = extracts[key]

          for feature in feat:
            ffi.write(str(feature) + ' ')
          for inten in intensity:
            ffi.write(str(inten) + ' ')
          ffi.write('\n')
      ffi.close()
      fe.close()
    step += 1
  print(error)

features_and_intensity('../Search_Results/LabelFree_Result_CPTAC',
                       charge=2, length=11, qvalue=0.01, ion_type='b')
features_and_intensity('../Search_Results/LabelFree_Result_PRIDE',
                       charge=2, length=11, qvalue=0.01, ion_type='b')
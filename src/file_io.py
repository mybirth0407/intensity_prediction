"""
Reading tsv file
"""

import csv
import re

def read_data():
  p = re.compile("[^a-zA-Z]")
  with open("../SulfenM/mzid/MSGF_MergedFDR.tsv", 'r') as tsv:
    tsv = csv.reader(tsv, delimiter='\t')
    # First line is 
    next(tsv)

    peptide = []
    charge = []
    for line in tsv:
      # ABC+333D -> ABCD
      reg_pep = p.sub('', line[9])
      if reg_pep != line[9]:
        continue

      # charge
      charge.append(line[8])
      # peptide
      peptide.append(line[9])
    return peptide, charge

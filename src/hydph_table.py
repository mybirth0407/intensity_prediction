"""
Hydrophobicity table of amino acids
"""

def get_aa_hydph(aa):
  return aa_hydph_table[aa]

aa_hydph_table = {
  'A' : 0.16,
  'C' : 2.50,
  'D' : -2.49,
  'E' : -1.50,
  'F' : 5.00,
  'G' : -3.31,
  'H' : -4.63,
  'I' : 4.41,
  'K' : -5.00,
  'L' : 4.76,
  'M' : 3.23,
  'N' : -3.79,
  'P' : -4.92,
  'Q' : -2.76,
  'R' : -2.77,
  'S' : -2.85,
  'T' : -1.08,
  'V' : 3.02,
  'W' : 4.88,
  'Y' : 2.00
}
"""
Feature extraction from peptides
"""

import mass_table
import hydph_table

class Peptide:
  def __init__(self, peptide, charge):
    self.peptide = peptide
    self.charge = charge

  """
  Peak location features
  """
  def location_min_mass(self, charge):

  def location_max_mass(self, charge):

  def location_relative(self, charge, x):

  """
  Peptide composition features
  """
  # number of x from n-term to i - 3
  def n_x(self, i, x):

  # number of x from i + 3 to c-term
  def c_x(self, i, x):

  """
  Hydrophobicity
  """
  # The sum of the hydrophobic amino acids in the peptide
  def hydf(self):

  # The average hydrophobicity of the amino acids
  # on both sides of fragmentation site
  def hydpra(self):

  # Differences in the hydrophobicity of amino acids
  # on both sides of fragmentation site
  def hydprd(self):

  # Hydrophobicity of the amino acid at the x-distance
  # from the fragmentation site to the c-term
  def hydn_x(self, x):

  # Hydrophobicity of the amino acid at the x-distance
  # from the fragmentation site to the n-term
  def hydc_x(self, x):

  """
  Peptide common features
  """
  # n term is x
  def nterm_is_x(self, x):

  # c term is x
  def cterm_is_x(self, x):

  # hydph sum of peptide
  def hydp(self):

if __name__ == "__main__":
  main()
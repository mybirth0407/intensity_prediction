"""
Feature extraction from peptides
"""

import mass_table as mass
import hydph_table as hydph

class Peptide:
  def __init__(self, peptide, charge):
    self.peptide = peptide
    self.charge = charge
    self.length = len(peptide)
    self.min = self.min_mass(self)
    self.max = self.max_mass(self)

  def min_mass(self):
    b = mass.get_aa_mass(self.peptide[0])
    y = mass.get_aa_mass(self.peptide[self.length - 1])
    return min(b, y)

  def max_mass(self):
    b = 0
    y = 0
    for i in (0, len(self.peptide) - 1):
      b += mass.get_aa_mass(self.peptide[i])
      y += mass.get_aa_mass(self.peptide[i + 1])
    return max(b, y)

  """
  Peak location features
  """
  def min_peak_mass(self, peak):
    if 0 < peak and peak < len(self.peptide):
      return mass.get_aa_mass(self.peptide[peak]) - self.min

  def max_peak_mass(self, peak):
    if 0 < peak and peak < len(self.peptide):
      return self.max - mass.get_aa_mass(self.peptide[peak])

  def relative_peak_mass(self, peak):
    return (self.peptide[peak] - min_peak_mass(peak))\
         / (max_peak_mass(peak) - min_peak_mass(peak))

  """
  Peptide composition features
  """
  # number of x from n-term to i - 3
  def n_x(self, i, x):
    if 0 < i - 3:
      s = 0
      for n in (0, i - 3):
        if aa == x:
          s += 1
      return s

  # number of x from i + 3 to c-term
  def c_x(self, i, x):
    if len(self.peptide) > i + 3:
      s = 0
      for n in (i + 3, len(self.peptide)):
        if aa == x:
          s += 1
      return s

  """
  Hydrophobicity
  """
  # The sum of the hydrophobic amino acids in the peptide
  def hydf(self):
    s = 0
    for aa in self.peptide:
      hydph = hydph.get_aa_hydph(aa)
      if hydph > 0:
        s += hydph
    return s

  # The average hydrophobicity of the amino acids
  # on both sides of fragmentation site
  def hydpra(self, fragmentation_site):
    if 0 < fragmentation_site and fragmentation_site < len(self.peptide):
      return (self.peptide[fragmentation_site]
            + self.peptide[fragmentation_site - 1]) / 2

  # Differences in the hydrophobicity of amino acids
  # on both sides of fragmentation site
  def hydprd(self, fragmentation_site):
    if 0 < fragmentation_site and fragmentation_site < len(self.peptide):
      return abs(self.peptide[fragmentation_site]
               - self.peptide[fragmentation_site - 1])


  # Hydrophobicity of the amino acid at the x-distance
  # from the fragmentation site to the c-term
  def hydn_x(self, fragmentation_site, x):
    if 0 < fragmentation_site - x and fragmentation_site < len(self.peptide):
      return hydph.get_aa_hydph(self.peptide[fragmentation_site - x])

  # Hydrophobicity of the amino acid at the x-distance
  # from the fragmentation site to the n-term
  def hydc_x(self, fragmentation_site, x):
    if 0 < fragmentation_site and len(self.peptide) >= fragmentation_site + x:
      return hydph.get_aa_hydph(self.peptide[fragmentation_site + x])

  """
  Peptide common features
  """
  # n term is x
  def nterm_is_x(self, x):
    if self.peptide[0] == x:
      return 1
    return 0

  # c term is x
  def cterm_is_x(self, x):
    if self.peptide[self.length - 1] == x:
      return 1
    return 0

  # hydph sum of peptide
  def hydp(self):
    s = 0
    for aa in self.peptide:
      s += hydph.get_aa_hydph(aa)
    return s

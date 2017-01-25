"""
Feature extraction from peptides
"""

import mass_table as mass
import hydph_table as hydph
import numpy as np
from data_reader import read_data
import re

# DLGLPTEAYISVEEVHDDGTPTSK
# LAPITSDPTEATAVGAVEASFK

class Peptide:
  def __init__(self, peptide, charge):
    self.peptide = self.get_strip_sequence(peptide)
    self.charge = charge
    self.length = len(self.peptide)
    self.min = self.min_mass()
    self.max = self.max_mass()

  def get_peak_features(self, ion_type):
    features_vector = np.mat(())
    for i in range(0, self.length):
      # feature for one peak

      # peptide composition features


      l = []
      # peak location features
      l.append(max_peak_mass(peak))
      l.append(relative_peak_mass(peak))

      # hydrophobicity features
    return features_vector
    
  # get strip sequence
  def get_strip_sequence(self, peptide):
    p = re.compile("[^a-zA-Z]")
    return p.sub('', peptide)
  
  # min(b1 ion, y1 ion)
  def min_mass(self):
    b = mass.get_aa_mass(self.peptide[0])
    y = mass.get_aa_mass(self.peptide[self.length - 1])
    return min(b, y)

  def max_mass(self):
    b = 0
    y = 0
    for i in range(0, len(self.peptide) - 1):
      b += mass.get_aa_mass(self.peptide[i])
      y += mass.get_aa_mass(self.peptide[i + 1])
    return max(b, y)

  """
  Peak location features
  """
  def min_peak_mass(self, peak):
    if -1 < peak and peak < self.length:
      return mass.get_aa_mass(self.peptide[peak]) - self.min
    return -1

  def max_peak_mass(self, peak):
    if -1 < peak and peak < self.length:
      return self.max - mass.get_aa_mass(self.peptide[peak])
    return -1

  def relative_peak_mass(self, peak):
    if -1 < peak and peak < self.length:
      return (mass.get_aa_mass(self.peptide[peak]) - self.min_peak_mass(peak))\
           / (self.max_peak_mass(peak) - self.min_peak_mass(peak))
    return -1

  """
  Peptide composition features

  n_x, c_x: how to define i, x
  """
  # number of x from n-term to i - 3
  def n_x(self, i, x):
    if 0 < i - 3 and i - 3 < self.length:
      s = 0
      for n in range(0, i - 3):
        if aa == x:
          s += 1
      return s
    return None

  # number of x from i + 3 to c-term
  def c_x(self, i, x):
    if 0 < i + 3 and i + 3 < self.length:
      s = 0
      for n in range(i + 3, self.length):
        if aa == x:
          s += 1
      return s
    return None

  """
  Hydrophobicity
  """
  # The sum of the hydrophobic amino acids in the fragment
  def hydf(self, fragmentation_site, ion_type):
    if fragmentation_site > self.length:
      return None
      
    s = 0
    if ion_type == 'b':
      for i in range(0, fragmentation_site):
        h = hydph.get_aa_hydph(self.peptide[i])
        s += h
    elif ion_type == 'y':
      for i in range(fragmentation_site, self.length - 1):
        s += h
    return s

  # The average hydrophobicity of the amino acids
  # on both sides of fragmentation site
  def hydpra(self, fragmentation_site):
    if 0 < fragmentation_site and fragmentation_site < self.length:
      return (hydph.get_aa_hydph(self.peptide[fragmentation_site])
            + hydph.get_aa_hydph(self.peptide[fragmentation_site - 1])) / 2
    return None

  # Differences in the hydrophobicity of amino acids
  # on both sides of fragmentation site
  def hydprd(self, fragmentation_site):
    if 0 < fragmentation_site and fragmentation_site < self.length:
      return abs(hydph.get_aa_hydph(self.peptide[fragmentation_site])
               - hydph.get_aa_hydph(self.peptide[fragmentation_site - 1]))
    return None

  # Hydrophobicity of the amino acid at the x-distance
  # from the fragmentation site to the c-term
  def hydn_x(self, fragmentation_site, x):
    if 0 < fragmentation_site - x and fragmentation_site < self.length:
      return hydph.get_aa_hydph(self.peptide[fragmentation_site - x])
    return None

  # Hydrophobicity of the amino acid at the x-distance
  # from the fragmentation site to the n-term
  def hydc_x(self, fragmentation_site, x):
    if 0 < fragmentation_site and fragmentation_site + x <= self.length:
      return hydph.get_aa_hydph(self.peptide[fragmentation_site + x])
    return None

  """
  Peptide common features
  """
  def get_peptide_features(self):
    return np.mat((nterm_is_x(), cterm_is_x(), hydp()))

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

"""
Feature extraction from peptides
"""

import mass_table as mass
import hydph_table as hydph
import aa_table as aa
import numpy as np
import file_io as f
import re

# DLGLPTEAYISVEEVHDDGTPTSK
# LAPITSDPTEATAVGAVEASFK

class Peptide:
  def __init__(self, peptide, charge, scan_num):
    self.peptide = self.get_strip_sequence(peptide)
    self.charge = charge
    self.length = len(self.peptide)
    self.min = self.min_mass()
    self.max = self.max_mass()
    self.scan_num = scan_num

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


  def get_peak_features(self, peak, fragmentation_site, ion_type, x):
    features_vector = []
    return features_vector
    

  """
  Peak location features (3 * 1)
  """ 
  # (3 * 1)
  def get_peak_location_features(self, peak):
    return np.mat((
        self.min_peak_mass(peak),
        self.max_peak_mass(peak),
        self.relative_peak_mass(peak)
    ))

  # (1 * 1)
  def min_peak_mass(self, fragmentation_site, ion_type):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    peak_mass = 0
    if ion_type == 'b':
      for i in range(0, fragmentation_site):
        peak_mass += mass.get_aa_mass(self.peptide[i])
    elif ion_type == 'y':
      for i in range(fragmentation_site, self.length):
        peak_mass += mass.get_aa_mass(self.peptide[i])
    return peak_mass - self.min

  # (1 * 1)
  def max_peak_mass(self, fragmentation_site, ion_type):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    peak_mass = 0
    if ion_type == 'b':
      for i in range(0, fragmentation_site):
        peak_mass += mass.get_aa_mass(self.peptide[i])
    elif ion_type == 'y':
      for i in range(fragmentation_site, self.length):
        peak_mass += mass.get_aa_mass(self.peptide[i])
    return self.max - peak_mass

  # (1 * 1)
  def relative_peak_mass(self, fragmentation_site, ion_type):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    peak_mass = 0
    if ion_type == 'b':
      for i in range(0, fragmentation_site):
        peak_mass += mass.get_aa_mass(self.peptide[i])
    elif ion_type == 'y':
      for i in range(fragmentation_site, self.length):
        peak_mass += mass.get_aa_mass(self.peptide[i])

    return (peak_mass - self.min_peak_mass(fragmentation_site))\
         / (self.max_peak_mass(fragmentation_site)
          - self.min_peak_mass(fragmentation_site))


  """
  Peptide composition features ()
  """
  # (40 * 1)
  def get_composition_features(self, fragmentation_site):
    return np.mat((n_x(fragmentation_site) + c_x(fragmentation_site)))

  # number of x from n-term to fragmentation_site
  # (20 * 1)
  def n_x(self, fragmentation_site):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    vector = [0] * 20
    # amino acids before fragmentation site
    for i in range(0, fragmentation_site):
      vector[ord(self.peptide[i]) - 64] += 1
    return vector

  # number of x from i + 3 to fragmentation_site
  # (20 * 1)
  def c_x(self, fragmentation_site):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    vector = [0] * 20
    # amino acids after fragmentation site
    for i in range(fragmentation_site, self.length):
      vector[ord(self.peptide[i]) - 64] += 1
    return vector


  """
  Hydrophobicity
  """
  # (5 * 1)
  def get_hyd_features(self, fragmentation_site, ion_type, x):
    return np.mat((
        self.hydf(fragmentation_site, ion_type),
        self.hydpra(fragmentation_site),
        self.hydprd(fragmentation_site),
        self.hydn_x(fragmentation_site, x),
        self.hydc_x(fragmentation_site, x)
    ))

  # The sum of the hydrophobic amino acids in the fragment
  # (1 * 1)
  def hydf(self, fragmentation_site, ion_type):
    if 0 < fragmentation_site and fragmentation_site < self.length:
      s = 0
      if ion_type == 'b':
        for i in range(0, fragmentation_site):
          h = hydph.get_aa_hydph(self.peptide[i])
          s += h
      elif ion_type == 'y':
        for i in range(fragmentation_site, self.length - 1):
          h = hydph.get_aa_hydph(self.peptide[i])
          s += h
      return s

  # The average hydrophobicity of the amino acids
  # on both sides of fragmentation site
  # (1 * 1)
  def hydpra(self, fragmentation_site):
    if 0 < fragmentation_site and fragmentation_site < self.length:
      return (hydph.get_aa_hydph(self.peptide[fragmentation_site])
            + hydph.get_aa_hydph(self.peptide[fragmentation_site - 1])) / 2
    return 0

  # Differences in the hydrophobicity of amino acids
  # on both sides of fragmentation site
  # (1 * 1)
  def hydprd(self, fragmentation_site):
    if 0 < fragmentation_site and fragmentation_site < self.length:
      return hydph.get_aa_hydph(self.peptide[fragmentation_site])\
           - hydph.get_aa_hydph(self.peptide[fragmentation_site - 1])
    return 0

  # Hydrophobicity of the amino acid at the x-distance
  # from the fragmentation site to the c-term
  # (1 * 1)
  def hydn_x(self, fragmentation_site, x):
    if 0 < fragmentation_site - x and fragmentation_site < self.length:
      return hydph.get_aa_hydph(self.peptide[fragmentation_site - x])
    return 0

  # Hydrophobicity of the amino acid at the x-distance
  # from the fragmentation site to the n-term
  # (1 * 1)
  def hydc_x(self, fragmentation_site, x):
    if 0 < fragmentation_site and fragmentation_site + x < self.length:
      return hydph.get_aa_hydph(self.peptide[fragmentation_site + x])
    return 0


  """
  Peptide common features
  """
  # (41 * 1)
  def get_peptide_common_features(self):
    return np.mat((self.nterm_is_x(), self.cterm_is_x(), self.hydp()))

  # n term is x
  # (20 * 1)
  def nterm_is_x(self):
    vector = [0] * 20
    for i in range(0, 20):
      if self.peptide[0] == aa.get_aa(i):
        vector[i] += 1
    return vector

  # c term is x
  # (20 * 1)
  def cterm_is_x(self):
    vector = [0] * 20
    for i in range(0, 20):
      if self.peptide[self.length - 1] == aa.get_aa(i):
        vector[i] += 1
    return vector

  # hydph sum of peptide
  # (1 * 1)
  def hydp(self):
    s = 0
    for aa in self.peptide:
      s += hydph.get_aa_hydph(aa)
    return s

p, c = f.read_tsv()
pp = Peptide(p[0], c[0], 0)
print(pp.get_peptide_common_features())
print(pp.get_hyd_features(2, 'b', 3))

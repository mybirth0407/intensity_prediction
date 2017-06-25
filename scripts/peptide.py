"""
Feature extraction from peptides
"""

import mass_table as mass
import hydph_table as hydph
import aa_table as aa
import numpy as np
import re

class Peptide:
  def __init__(self, peptide, charge, ion_type):
    self.peptide = self.get_strip_sequence(peptide)
    self.charge = charge
    self.ion_type = ion_type
    self.length = len(self.peptide)
    self.min = self.min_mass()
    self.max = self.max_mass()

  # get strip sequence
  def get_strip_sequence(self, peptide):
    p = re.compile("[^a-zA-Z]")
    return p.sub('', peptide)
  
  # min(b1 ion, y1 ion)
  def min_mass(self):
    b = mass.get_aa_mass(self.peptide[0])
    y = mass.get_aa_mass(self.peptide[self.length - 1])
    return min(b, y)

  # max(b1 ion, y1 ion)
  def max_mass(self):
    b = 0
    y = 0
    for i in range(len(self.peptide) - 1):
      b += mass.get_aa_mass(self.peptide[i])
      y += mass.get_aa_mass(self.peptide[i + 1])
    return max(b, y)


  def get_features(self):
    features_vector = []

    for i in range(1, self.length):
      features_vector.extend(self.get_peak_location_features(i, self.ion_type))
      features_vector.extend(self.get_composition_features(i))
      features_vector.extend(self.get_hyd_features(i, self.ion_type, 1))
    features_vector.extend(self.get_peptide_common_features())
    return features_vector


  """
  Peak location features
  """ 
  # (3 * 1)
  def get_peak_location_features(self, fragmentation_site, ion_type):
    # [float, float, float]
    return [self.min_peak_mass(fragmentation_site, ion_type),
            self.max_peak_mass(fragmentation_site, ion_type),
            self.relative_peak_mass(fragmentation_site, ion_type)]

  # (1 * 1)
  def min_peak_mass(self, fragmentation_site, ion_type):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    peak_mass = 0
    if ion_type == 'b':
      for i in range(fragmentation_site):
        if self.peptide[i] == 'C':
          peak_mass += 57.02146

        peak_mass += mass.get_aa_mass(self.peptide[i])
    elif ion_type == 'y':
      for i in range(fragmentation_site, self.length):
        if self.peptide[i] == 'C':
          peak_mass += 57.02146

        peak_mass += mass.get_aa_mass(self.peptide[i])
    return peak_mass - self.min

  # (1 * 1)
  def max_peak_mass(self, fragmentation_site, ion_type):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    peak_mass = 0
    if ion_type == 'b':
      for i in range(fragmentation_site):
        if self.peptide[i] == 'C':
          peak_mass += 57.02146

        peak_mass += mass.get_aa_mass(self.peptide[i])
    elif ion_type == 'y':
      for i in range(fragmentation_site, self.length):
        if self.peptide[i] == 'C':
          peak_mass += 57.02146

        peak_mass += mass.get_aa_mass(self.peptide[i])
    return self.max - peak_mass

  # (1 * 1)
  def relative_peak_mass(self, fragmentation_site, ion_type):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    peak_mass = 0
    if ion_type == 'b':
      for i in range(fragmentation_site):
        if self.peptide[i] == 'C':
          peak_mass += 57.02146

        peak_mass += mass.get_aa_mass(self.peptide[i])
    elif ion_type == 'y':
      for i in range(fragmentation_site, self.length):
        if self.peptide[i] == 'C':
          peak_mass += 57.02146

        peak_mass += mass.get_aa_mass(self.peptide[i])

    # (peak_mass - min peak) / (max peak - min peak) 
    return (peak_mass
          - self.min_peak_mass(fragmentation_site, ion_type))\
         / (self.max_peak_mass(fragmentation_site, ion_type)
          - self.min_peak_mass(fragmentation_site, ion_type))


  """
  Peptide composition features
  """
  # (40 * 1)
  def get_composition_features(self, fragmentation_site):
    # [] + []
    return self.n_x(fragmentation_site) + self.c_x(fragmentation_site)

  # number of x from n-term to fragmentation_site
  # (20 * 1)
  def n_x(self, fragmentation_site):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    vector = [0] * 20
    # amino acids before fragmentation site
    for i in range(fragmentation_site):
      vector[aa.get_aa(self.peptide[i])] += 1
    return vector

  # number of x from i + 3 to fragmentation_site
  # (20 * 1)
  def c_x(self, fragmentation_site):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    vector = [0] * 20
    # amino acids after fragmentation site
    for i in range(fragmentation_site, self.length):
      vector[aa.get_aa(self.peptide[i])] += 1
    return vector


  """
  Peptide Hydrophobicity Features
  """
  # (7 * 1)
  def get_hyd_features(self, fragmentation_site, ion_type, distance):
    # float, float, float, float, float, float, float
    return [self.hydf(fragmentation_site, ion_type),
            self.hydpra(fragmentation_site),
            self.hydprd(fragmentation_site),
            self.hydn_x(fragmentation_site, distance),
            self.hydc_x(fragmentation_site, distance),
            self.hydn_fragmentation_site(fragmentation_site),
            self.hydc_fragmentation_site(fragmentation_site)]

  # The sum of the hydrophobic amino acids in the fragment
  # (1 * 1)
  def hydf(self, fragmentation_site, ion_type):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    s = 0
    if ion_type == 'b':
      for i in range(fragmentation_site):
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
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    return (hydph.get_aa_hydph(self.peptide[fragmentation_site])
          + hydph.get_aa_hydph(self.peptide[fragmentation_site - 1])) / 2

  # Differences in the hydrophobicity of amino acids
  # on both sides of fragmentation site
  # (1 * 1)
  def hydprd(self, fragmentation_site):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    return hydph.get_aa_hydph(self.peptide[fragmentation_site])\
         - hydph.get_aa_hydph(self.peptide[fragmentation_site - 1])


  # Hydrophobicity of the amino acid at the x-distance
  # from the fragmentation site to the c-term
  # (1 * 1)
  def hydn_x(self, fragmentation_site, distance):
    if fragmentation_site - distance <= 0\
      or fragmentation_site - distance >= self.length:
      return 0

    return hydph.get_aa_hydph(self.peptide[fragmentation_site - distance])

  # Hydrophobicity of the amino acid at the x-distance
  # from the fragmentation site to the n-term
  # (1 * 1)
  def hydc_x(self, fragmentation_site, distance):
    if fragmentation_site + distance <= 0\
      or fragmentation_site + distance >= self.length:
      return 0

    return hydph.get_aa_hydph(self.peptide[fragmentation_site + distance])

  # Hydrophobicity of the amino acid at the fragmentation site to n-term
  # (1 * 1)
  def hydn_fragmentation_site(self, fragmentation_site):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    return hydph.get_aa_hydph(self.peptide[fragmentation_site - 1])

  # Hydrophobicity of the amino acid at the fragmentation site to c-term
  # (1 * 1)
  def hydc_fragmentation_site(self, fragmentation_site):
    if fragmentation_site <= 0 or fragmentation_site >= self.length:
      return 0

    return hydph.get_aa_hydph(self.peptide[fragmentation_site])


  """
  Peptide common features
  """
  # (41 + 21 * (peptide length)
  def get_peptide_common_features(self):
    # [] + [] + [float] + [] + []
    return self.nterm_is_x() + self.cterm_is_x() + [self.hydp()]\
         + self.sequence_info() + self.sequence_hydph_info()

  # n term is x
  # (20 * 1)
  def nterm_is_x(self):
    vector = [0] * 20
    vector[aa.get_aa(self.peptide[0])] = 1
    return vector

  # c term is x
  # (20 * 1)
  def cterm_is_x(self):
    vector = [0] * 20
    vector[aa.get_aa(self.peptide[self.length - 1])] = 1
    return vector

  # Hydph sum of peptide
  # (1 * 1)
  def hydp(self):
    s = 0
    for aa in self.peptide:
      s += hydph.get_aa_hydph(aa)
    return s

  # Intuitive sequence information
  # (20 * peptide length)
  def sequence_info(self):
    # peptide length limit is 11
    vector = []
    for i in range(self.length):
      v = [0] * 20
      v[aa.get_aa(self.peptide[i])] = 1
      vector.extend(v)
    return vector

  # Intuitive peptide hydrophobicity information
  # (peptide length * 1)
  def sequence_hydph_info(self):
    vector = []
    for i in range(self.length):
      vector.append(hydph.get_aa_hydph(self.peptide[i]))
    return vector

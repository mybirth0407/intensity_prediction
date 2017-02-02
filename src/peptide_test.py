from peptide import *
import pytest


class PeptideTest:
  def __init__(self):
    self.pt = Peptide("DLGLPTEAYISVEEVHDDGTPTSK", 3, 12026)

  def test_peak_location_features(self):
    assert self.pt.get_peak_location_features(1, 'b')

  def test_composition_features(self):
    assert self.pt.get_composition_features(1)

  def test_hyd_features(self):
    assert self.pt.get_hyd_features(1, 'b', 3)

  def test_peptide_common_features(self):
    assert self.pt.get_peptide_common_features(1)


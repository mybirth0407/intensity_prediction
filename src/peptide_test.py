"""
Peptide test class
"""
import pytest
import numpy as np
import peptide

p1 = peptide.Peptide('PMFIVNTNVPR', 2)
p2 = peptide.Peptide('YALYDATYETK', 2)

def pytest_generate_tests(metafunc):
  # called once per each test function
  funcarglist = metafunc.cls.params[metafunc.function.__name__]
  argnames = sorted(funcarglist[0])
  metafunc.parametrize(argnames,
      [[funcargs[name] for name in argnames] for funcargs in funcarglist])

class TestClass:
  # a map specifying multiple argument sets for a test method
  params = {
    'test_min_peak_mass': [dict(fs=1, ion='b')]
    # 'test_peak_location_features': [dict(fs=1, ion='b'), ],
    # 'test_composition_features': [dict(fs=1), ],
    # 'test_hyd_features': [dict(fs=1, ion='b', d=1), ],
    # 'test_peptide_common_features': [dict(), ]
  }
  def test_min_peak_mass(self, fs, ion):
    assert p1.min_peak_mass(fs, ion) == 0
    assert p2.min_peak_mass(fs, ion) == 0

  # def test_peak_location_features(self, fs, ion):

  # def test_composition_features(self, fs):

  # def test_hyd_features(self, fs, ion, d):

  # def test_peptide_common_features(self):


# 128.09496
# 163.06333
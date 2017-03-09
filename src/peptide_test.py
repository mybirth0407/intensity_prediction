"""
Peptide test class
"""
import pytest
import numpy as np
import peptide

p = peptide.Peptide('YALYDATYETK', 2)

def pytest_generate_tests(metafunc):
  # called once per each test function
  funcarglist = metafunc.cls.params[metafunc.function.__name__]
  argnames = sorted(funcarglist[0])
  metafunc.parametrize(argnames, [[funcargs[name] for name in argnames] 
      for funcargs in funcarglist])

class TestClass:
  # a map specifying multiple argument sets for a test method
  params = {
    'test_equals': [dict(a=1, b=2), dict(a=3, b=3), ],
    'test_zerodivision': [dict(a=1, b=0), ],
    'test_peak_location_features': [dict(fs=1, ion='b'), ],
    'test_composition_features': [dict(fs=1), ],
    'test_hyd_features': [dict(fs=1, ion='b', d=1), ],
    'test_peptide_common_features': [dict(), ]
  }

  def test_peak_location_features(self, fs, ion):

  def test_composition_features(self, fs):

  def test_hyd_features(self, fs, ion, d):

  def test_peptide_common_features(self):

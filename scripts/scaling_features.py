"""
TODO
"""

import sys
import os
import numpy as np



def make_scaling_features(input_file, result_file):
  data = np.loadtxt(input_file, dtype='float32')
  f_result = open(result_file, 'wt', encoding='utf-8')

make_scaling_features(sys.argv[1], sys.argv[2])
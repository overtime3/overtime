"""
Overtime
========

Overtime is a Python package for the creation and analysis of temporal networks.

"""

# check installed python version
import sys
if sys.version_info[:2] < (3, 7):
    m = "Python 3.7 or later is required for Overtime ({}.{} detected)."
    raise ImportError(m.format(sys.version_info[:2]))
del sys



# imports
import overtime.components
from overtime.components import *

import overtime.inputs
from overtime.inputs import *

import overtime.generators
from overtime.generators import *

import overtime.plots
from overtime.plots import *

import overtime.algorithms
from overtime.algorithms import *

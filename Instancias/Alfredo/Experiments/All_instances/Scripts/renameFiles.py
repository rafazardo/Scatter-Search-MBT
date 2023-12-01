import multiprocessing 
import time 
import glob
import sys
from parse import parse
import argparse
import os
from os import path
import math
import networkx as nx
import matplotlib.pyplot as plt
import os.path
import statistics
import numpy as np
import math
import re

path = '../Inputs/'
outputs = sorted([_ for _ in glob.glob(path + f'*.in')])

for output in outputs:
	if 'MBG' in output:
		new_name = output.replace('MBG_', '')
		os.system(f'mv {output} {new_name}')
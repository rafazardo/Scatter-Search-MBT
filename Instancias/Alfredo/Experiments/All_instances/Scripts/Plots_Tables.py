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

cut_off = 60

def getData(nameFile):
	file = open(nameFile)
	line = None
	while True:
		line = list(file.readline().split())
		if line[0] == 'MBT:':
			break
	mbt = int(line[1])
	tb = float((list(file.readline().split()))[4])
	tt = float((list(file.readline().split()))[2])
	it = int((list(file.readline().split()))[1])
	# print(nameFile, mbt, tb, tt, it)
	return mbt, tb, tt, it

# Raw data
mbts = {}
ttts = {}
times = {}
its = {}

# Reference values
best_mbt = {}
best_mean_mbt = {}

max_time = {}
qt_best_mbt = {}
qt_best_mbt_mean = {}


# Refined data
ttts_plot = {}

path = '../Outputs/'
outputs = sorted([_ for _ in glob.glob(path + f'*.out')])

algorithms = {
	'BRKGA': ['H0', 'HI0', 'HO0', 'HOI0']	
	# 'BRKGA': ['H0', 'H1', 'H2', 'H3']	
	# 'BRKGA': ['HO0', 'HO1', 'HO2', 'HO3']	
	# 'BRKGA': ['H0', 'H2', 'HO0', 'HO2']	
	# 'BRKGA': ['H2', 'HO2']	
	# 'BRKGA': ['H0', 'H1', 'H2', 'H3', 'HO0', 'HO1', 'HO2', 'HO3']	
}

query = ''
for i,a in enumerate(algorithms.keys()):
	if i : query += '|' 
	query += a

instances = set()

for output in outputs:
	if 'RT' in output: continue
	if 'BT0_' in output: continue
	if 'BT1_' in output: continue
	if 'BT2_' in output: continue
	if 'BT3_' in output: continue
	if 'BT4_' in output: continue
	if 'BT5_' in output: continue
	if 'BT6_' in output: continue
	if 'BT7_' in output: continue
	if 'BT8_' in output: continue
	if 'BT9_' in output: continue
	# output = output.replace(path,'')
	a = re.search(query,output)
	instances.add(output[:a.start()])

for alg in algorithms.keys():
	qt_best_mbt[alg] = {}
	qt_best_mbt_mean[alg] = {}
	for var in algorithms[alg]:
		qt_best_mbt[alg][var] = 0
		qt_best_mbt_mean[alg][var] = 0


for inst in sorted(instances):
	mbts[inst] = {}
	ttts[inst] = {}
	times[inst] = {}
	its[inst] = {}
	ttts_plot[inst] = {}
	best_mbt[inst] = 1<<20
	best_mean_mbt[inst] = 1<<20

	for alg in algorithms.keys():
		mbts[inst][alg] = {}
		ttts[inst][alg] = {}
		times[inst][alg] = {}
		its[inst][alg] = {}
		ttts_plot[inst][alg] = {}

		for var in algorithms[alg]:
			mbts[inst][alg][var] = []
			ttts[inst][alg][var] = []
			times[inst][alg][var] = []
			its[inst][alg][var] = []
			ttts_plot[inst][alg][var] = []

			pattern = f'{inst}*{alg}*{var}*'
			nameFiles = sorted([_ for _ in glob.glob(path + pattern)])
			for nameFile in nameFiles:
				mbt, tb, tt, it = getData(nameFile)
				mbts[inst][alg][var].append(mbt)
				ttts[inst][alg][var].append(tb)
				times[inst][alg][var].append(tt)
				its[inst][alg][var].append(it)
				best_mbt[inst] = min(best_mbt[inst], mbt)


# Processing raw data
for inst in sorted(instances):
	for alg in algorithms.keys():
		for var in algorithms[alg]:
			best_mean_mbt[inst] = min(best_mean_mbt[inst], statistics.mean(mbts[inst][alg][var])) 
			for i,tb in enumerate(ttts[inst][alg][var]):
				ttts_plot[inst][alg][var].append( 
					tb
					if mbts[inst][alg][var][i] == best_mbt[inst] 
					else cut_off
					)


file = open(f'Table_H0-HI0-HO0-HOI0_WT.txt', 'w')

for inst in sorted(instances):
	name = inst.replace(path,'')[0:-1]
	name = name.replace('_','-')
	file.write(f'{name}')
	for alg in sorted(algorithms.keys()):
		for var in algorithms[alg]:
			min_mbt = min(mbts[inst][alg][var])
			mean = statistics.mean(mbts[inst][alg][var])

			if min_mbt == best_mbt[inst] :
				qt_best_mbt[alg][var] += 1
			
			if mean == best_mean_mbt[inst]:
				qt_best_mbt_mean[alg][var] += 1

			file.write(f' & ')

			if min_mbt == best_mbt[inst]:
				file.write(f'\\textbf{"{"}')
			file.write('{:d}'.format(min_mbt))
			if min_mbt == best_mbt[inst]:
				file.write(f'{"}"}')
			file.write(f' & ')

			if mean == best_mean_mbt[inst]:
				file.write(f'\\textbf{"{"}')
			file.write('{:.2f}'.format(statistics.mean(mbts[inst][alg][var])))
			if mean == best_mean_mbt[inst]:
				file.write(f'{"}"}')
			file.write(f' & ')
			file.write('{:.2f}'.format(statistics.mean(ttts_plot[inst][alg][var])))
			# file.write(f' & ')
			# file.write('{:.2f}'.format(statistics.mean(its[inst][alg][var])))
	file.write(f'\\\\ \n')


file.write(f'Best\\\\\n')
for alg in sorted(algorithms.keys()):
	for var in algorithms[alg]:
		file.write(f'{alg}-{var}: {qt_best_mbt[alg][var]}\\\\\n')

file.write(f'Best Mean\\\\\n')
for alg in sorted(algorithms.keys()):
	for var in algorithms[alg]:
		file.write(f'{alg}-{var}: {qt_best_mbt_mean[alg][var]}\\\\\n')

file.write(f'TOTAL: {len(instances)}\n')

#!/usr/bin/python

from __future__ import print_function
from __future__ import division

import random
# set up random

def fall_off(size, failure_chance):
	"""Uniform fall off
	
	   Returns a positive integer if the found fall_off is <= size.
	   Returns 0 otherwise
	"""
	assert 1 >= failure_chance >= 0, "Failure chance is outside percent range: %r" % failure_chance
	#let fall off rate be 5%
	#let size of gene be 200
	#find out if it falls off
	#20/0.05 == 4000
	#get random number in range 1-4000
	#if it is less than 200 then it falls off
	#len(gene) * (100 / (fall off rate * 100)) == top of range
	# TODO use non-normal distribution
	top_range = size / failure_chance
	fallen = random.randint(1, top_range)
	if fallen <= size: return fallen
	else: return 0

def simulate(dna, primer): # any others?
	# loop over # of cycles
	pass

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description="Simulate the pcr process at a fairly high level")
	# n - number of base pairs
	parser.add_argument('n', type=int)
	# m - size of DNA segment to be amplified
	parser.add_argument('m', type=int)
	# p - fixed primer length
	parser.add_argument('p', type=int)

	args = vars(parser.parse_args())


	# TODO generate dna, primer, etc.
	# TODO run simulation
	# TODO print or somehow return statistics, even on error
	pass

#!/usr/bin/python

from __future__ import print_function

import random
# set up random

def fall_off(size, failure_chance):
	#let fall off rate be 5%
	#let size of gene be 200
	#find out if it falls off
	#100/5 == 20
	#200*20 == 4000
	#get random number in range 1-4000
	#if it is less than 200 then it falls off
	#len(gene) * (100 / (fall off rate * 100)) == top of range
	# TODO use non-normal distribution
	pass

def simulate(dna, primer): # any others?
	# loop over # of cycles
	pass

if __name__ == '__main__':
	# TODO get data from cmd line args
	# TODO generate dna, primer, etc.
	# TODO run simulation
	# TODO print or somehow return statistics, even on error
	pass

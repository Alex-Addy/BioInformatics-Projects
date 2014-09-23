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

def simulate(dna, primer):
        # returns the new strand created even if
        # too short
        
        # get the starting index to copy
        # throw error if primer string not found
        start = dna.find(primer)
        assert start > -1, "Primer not found"

        length = len(dna)
        fallOff = fall_off(length, 0.05)

        if fallOff > length: return dna[start:]
        else: return dna[start:fallOff]

def get_primer(dna, index, length):
        # Gets the primer for the section to be
        # copied.  Index defines the beginning of
        # the section.

        # Check for copies of the bases found at
        # the beginning of the section.
        pos = find(dna, dna[index: index + length])
        if pos == index and find(dna, dna[index: index+length], pos+1):
                # didn't find any duplicates of the proposed primer elsewhere in the sequence
                return dna[index: index+length]

        # Looks for a suitable primer before the section
        # to be copied.
        else:
                primerFound = false
                searchIndex = index
                while not primerFound:
                      searchIndex+=1
                      assert searchIndex >= 0, "No suitable primer"
                      pos = find(dna, dna[searchIndex: searchIndex + length])
                      if pos == searchIndex: return dna[searchIndex: searchIndex + length]

def gen_dna(length):
        BASES = ['A', 'T', 'G', 'C']
        return str([random.choice(BASES) for _ in xrange(length)])


if __name__ == '__main__':
        import argparse
        parser = argparse.ArgumentParser(description="Simulate the pcr process at a fairly high level")
        parser.add_argument('n', type=int, "size of total dna segment, in base pairs")
        parser.add_argument('m', type=int, "size of DNA segment to analyze")
        parser.add_argument('p', type=int, "primer length")
        parser.add_argument('c', type=int, help="number of cycles to simulate")

        args = vars(parser.parse_args())

        dna = gen_dna(args['n'])
        cycles = 10

        # TODO generate primer
        # TODO check primer
        
        # iterate for number of cycles
        for x in xrange(0, cycles):
               simulate(dna, primer) 
        
        
        # TODO run simulation
        # TODO print or somehow return statistics, even on error
        pass

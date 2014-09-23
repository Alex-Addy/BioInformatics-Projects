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

def single_copy(source, primer, chance=0.05):
        # returns the new strand created even if
        # too short
        
        # get the starting index to copy
        # throw error if primer string not found
        start = source.find(primer)
        assert start > -1, "Primer not found"

        fallOff = fall_off(len(source), chance)

        if fallOff > len(source): return (dna,len(source))
        else: return (start,fallOff)

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
        return ''.join([random.choice(BASES) for _ in xrange(length)])

# segments is a dictionary containing a tuple of the slice ranges (x, y)
# and a value of the number of times it has been inserted into the dictionary
def simulate(segments, primer):
        new_segments = {} # contains all new generated segments
        for s in segments:
                # find primer
                # get falloff
                # add to dict, incrementing the value there
                #     look at the second argument of {}.get for one way to do this
                #     you could also just do a key in d, or key not in d, to do the check
        return new_segments


if __name__ == '__main__':
        import argparse
        parser = argparse.ArgumentParser(description="Simulate the pcr process at a fairly high level")
        parser.add_argument('n', type=int, "size of total dna segment, in base pairs")
        parser.add_argument('m', type=int, "size of DNA segment to analyze")
        parser.add_argument('p', type=int, "primer length")
        parser.add_argument('c', type=int, help="number of cycles to simulate")

        args = vars(parser.parse_args())

        dna = gen_dna(args['n'])

        # TODO generate primer
        
        new_segs = {dna}
        # iterate for number of cycles
        for x in xrange(0, args['c']):
                try:
                        new_segs = simulate(new_segs, primer)
                except:
                        print("Errored on cycle %d of %d." % (x, args['c']))
                        raise

        # TODO print or somehow return statistics, even on error
        pass

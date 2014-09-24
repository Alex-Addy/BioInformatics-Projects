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
        # Gets the primers for the section to be
        # copied.  Index defines the beginning of the section.

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
        strand = ''.join([random.choice(BASES) for _ in xrange(length)])
	new_s = strand.replace('A', 'K')
	new_s = new_s.replace('T', 'A')
	new_s = new_s.replace('K', 'T')

	new_s = new_s.replace('G', 'K')
	new_s = new_s.replace('C', 'G')
	new_s = new_s.replace('K', 'C')

	return (strand, new_s)

# segments is a dictionary containing a tuple of the slice ranges (x, y)
# and a value of the number of times it has been inserted into the dictionary
def simulate(segments, primer):
        new_segments = {} # contains all new generated segments
        for s in segments:
                # find primer
                primerIndex = find_primer_index_in_segment(segments, primer)
                # get falloff
                falloffIndex = -1
                # add to dict, incrementing the value there
                #     look at the second argument of {}.get for one way to do this
                #     you could also just do a key in d, or key not in d, to do the check
                if primerIndex != -1:
                        falloffIndex = find_falloff_index_in_segment(segments, primerIndex)
                        if (primerIndex, falloffIndex) in new_segments:
                                new_segments[(primerIndex, falloffIndex)] += 1
                        else:
                                new_segments[(primerIndex, falloffIndex)] = 1

                else:
                        if(primerIndex, len(segments)):        
                                new_segments[(primerIndex, len(segments))] += 1
                        else:
                                new_segments[(primerIndex, len(segments))] = 1
        return new_segments

def find_primer_index_in_segment(segments, primer):
                if primer in segments:
                        c = primer[0]
                        for ch in segments:
                                if ch == c:
                                        if segments[index:index+len(char)] == char:
                                                return index
                else:
                        return -1

def find_falloff_index_in_segment(segments, primerIndex):
        x = segments[primerIndex:]
        index = fall_off(x, chance=.05)
        if index != 0:
                return index + primerIndex
        else:
                return -1

def count_number_of_DNA_fragments_in_dictionary(new_segment):
        numberOfFragments = 0;
        for key in new_segment:
                number of Fragments += (new_segment[key])
        return numberOfFragments

def average_length_of_DNA_fragments_in_dictionary(new_segment, numberOfFragments):
        int combinedLength = 0;
        for key in new_segment:
                listOfTuples = list(key)
                combinedLength += listOfTuples[1] - listOfTuples[0];

        return combinedLength / numberOfFragments
                

def distribution_of_lengths_in_dictionary(new_segment):

        
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
                except Exception as e:
                        print("Errored on cycle %d of %d.\r\nWith error %s." % (x, args['c'], e.strerror))
                        break
		# do some stats on the dictionary
		
		# display the stats
	# print	aggregate stats

        pass

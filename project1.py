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

def reverse_strand(dnaStrand, geneIndex):
    # Reverses the dna strand and returns the new index for
    # the gene to be copied
    # Returns the reversed strand and new gene starting index

    newIndex = (len(dnaStrand) - 1) - geneIndex
    return (dnaStrand[::-1], newIndex)

def gen_dna(length):
    BASES = ['A', 'T', 'G', 'C']
    return ''.join([random.choice(BASES) for _ in xrange(length)])

# segments is a dictionary containing a tuple of the slice ranges (x, y)
# and a value of the number of times it has been inserted into the dictionary
def simulate(strandForward, strandBackward, primerForward, primerBackward):
    #strandForward is a dictionary
    #strandBackward is a dictionary
    #primerForward is a string
    #primerBackward is a string

    new_strandForward = {} # contains all new generated segments
    new_strandBackward = {}
    for s in strandForward:
        # find primer
        primerForwardIndex = find_primer_index_in_segment(strandForward, primerForward)
        # get falloff
        falloffForwardIndex = -1
        # add to dict, incrementing the value there
        #     look at the second argument of {}.get for one way to do this
        #     you could also just do a key in d, or key not in d, to do the check
        if primerForwardIndex != -1:
            falloffForwardIndex = find_falloff_index_forward_in_segment(strandForward, primerForwardIndex)
            if (primerForwardIndex, falloffForwardIndex) in new_strandForward:
                new_strandForward[(primerForwardIndex, falloffForwardIndex)] += 1
            else:
                new_strandForward[(primerForwardIndex, falloffForwardIndex)] = 1

        else:
            if(primerForwardIndex, len(strandForward)) in new_strandForward:
                new_strandForward[(primerForwardIndex, len(strandForward))] += 1
            else:
                new_strandForward[(primerForwardIndex, len(strandForward))] = 1

    for s in strandBackward:
        #find primer
        primerBackwardIndex = find_primer_backward_index_in_segment(segmentBackward, primerBackward)
        #get falloff
        falloffBackwardIndex = -1
        if primerBackwardIndex != -1:
            falloffBackwardIndex = find_falloff_index_backward_in_segment(strandBackward, primerBackwardIndex)
            if (falloffBackwardIndex, primerBackwardIndex) in new_strandBackward:
                new_strandBackward[(falloffBackwardIndex, primerBackwardIndex)] +=1
            else:
                new_strandBackward[(falloffBackwardIndex, primerBackwardIndex)] = 1

        else:
            if(0, primerBackwardIndex) in new_strandBackward:
                new_strandBackward[(0, primerBackwardIndex)] +=1
            else:
                new_strandBackward[(0, primerBackwardIndex)] = 1

    return new_strandForward, new_strandBackward

def find_primer_forward_index_in_segment(segments, primer):
    index = -1
    primerCompliment = create_compliment(primer)
    if primerCompliment in segment:
        index = segment.index(primer)
    return index


def find_primer_backward_index_in_segment(segment, primer):
    index = -1;
    reverseSegment = segment[::1]
    reversePrimer = primer[::1]
    if reversePrimer in reverseSegment:
        index = segments.index(primer)

def create_compliment(letters):
    newLetters
    newLetters = string.replace(letters, "A", "K")
    newLetters = string.replace(letters, "T", "L")
    newLetters = stirng.replace(letters, "K", "T")
    newLetters = string.replace(letters, "L", "A")

    newLetters = string.replace(letters, "C", "D")
    newLetters = string.replace(letters, "G", "E")
    newLetters = string.replace(letters, "D", "G")
    newLetters = string.replace(letters, "E", "C")

    return newLetters

def find_falloff_forward_index_in_segment(segments, primerIndex):
    x = len(segments[primerIndex:])
    index = fall_off(x, chance=.05)
    if index != 0:
        return index + primerIndex
    else:
        return -1

def find_falloff_backward_index_in_segment(segment, primerIndex):
    x = len(segments[:primerIndex])
    index = fall_off_back(x, chance=.05)
    if index != len(segment):
        return index
    else:
        return -1

def count_number_of_DNA_fragments_in_dictionary(new_segment):
    numberOfFragments = 0
    for key in new_segment:
        numberOfFragments += (new_segment[key])
    return numberOfFragments

def average_length_of_DNA_fragments_in_dictionary(new_segment, numberOfFragments):
    combinedLength = 0
    for key in new_segment:
        listOfTuples = list(key)
        combinedLength += listOfTuples[1] - listOfTuples[0]

    return combinedLength / numberOfFragments


def distribution_of_lengths_in_dictionary(new_segment):
    pass


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Simulate the pcr process at a fairly high level")
    parser.add_argument('n', type=int, help="size of total dna segment, in base pairs")
    parser.add_argument('m', type=int, help="size of DNA segment to analyze")
    parser.add_argument('p', type=int, help="primer length")
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
            print("Errored on cycle %d of %d.\r\nWith error %s." % (x, args['c'], e.message))
            break
        # do some stats on the dictionary

        # display the stats
    # print aggregate stats

    pass

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

    #Generate the two temporary dictionaries to hold the new strands
    new_strandForward = {} 
    new_strandBackward = {}
    for s in strandForward:
        # find primer
        primerForwardIndex = find_primer_forward_index_in_segment(s, primerForward)
        #if primer exists find falloff index, add to the correct temporary dictionary.
        if primerForwardIndex != -1:
            falloffForwardIndex = find_falloff_index_forward_in_segment(s, primerForwardIndex)
            if (primerForwardIndex, falloffForwardIndex) in new_strandBackward:
                new_strandBackward[(primerForwardIndex, falloffForwardIndex)] += 1
            else:
                new_strandBackward[(primerForwardIndex, falloffForwardIndex)] = 1

    for s in strandBackward:
        #find primer
        primerBackwardIndex = find_primer_backward_index_in_segment(s, primerBackward)
        #if primer exists find falloff index, add to the correct temporary dictionary.
        if primerBackwardIndex != -1:
            falloffBackwardIndex = find_falloff_index_backward_in_segment(s, primerBackwardIndex)
            if (falloffBackwardIndex, primerBackwardIndex) in new_strandForward:
                new_strandForward[(falloffBackwardIndex, primerBackwardIndex)] +=1
            else:
                new_strandForward[(falloffBackwardIndex, primerBackwardIndex)] = 1

    #return the two new dictionaries
    return new_strandForward, new_strandBackward

def find_primer_forward_index_in_segment(segment, primer):
    #Function is to initialy set index to -1.
    #Then it will create a compliment for the primer.
    #Then it will search the passed in segment of dna for said compliment.
    #If found, return the index of that primer.
    #Otherwise, return the -1 to represent no found complement for the primer.
    index = -1
    primerCompliment = create_compliment(primer)
    if primerCompliment in segment:
        index = segment.index(primer)
    return index


def find_primer_backward_index_in_segment(segment, primer):
    #Function is to initially set index to -1.
    #It will then reverse the passed in segment and primer.
    #This is because we want to search from back to front.
    #Then it will create a compliment for the reversed primer.
    #Then it will search the reversed segment for the reversed primer compliment.
    #if found, get that index, re-reverse the index and segment and return the index.
    #Otherwise return the -1 to represent no found complement for the primer.
    index = -1
    reverseSegment = segment[::1]
    reversePrimer = primer[::1]
    reversePrimerCompliment = create_compliment(reversePrimer)
    if reversePrimer in reverseSegment:
        index = segments.index(primer)
        (segment, index) = reverse_strand(reverseSegment, index)
    return index
    
def create_compliment(letters):
    #Function will create a compliment of the dna strand string passed in.
    newLetters = string.replace(letters, "A", "K")
    newLetters = newLetters.replace(letters, "T", "A")
    newLetters = newLetters.replace(letters, "K", "T")

    newLetters = newLetters.replace(letters, "C", "K")
    newLetters = newLetters.replace(letters, "G", "C")
    newLetters = newLetters.replace(letters, "K", "G")

    return newLetters

def find_falloff_forward_index_in_segment(segment, primerIndex):
    #Function will find the index where the PCR will fall off.
    #First, get the length of the segment.
    #Then, calculate the index of the fall off.  Index of 0 means no fall off.
    #if fall off exists, return the index from the fall off added onto the length of the strand up until the primer.
    #Otherwise, no fall off is found.  So the index will be the last character of the string.
    x = len(segment[primerIndex:])
    index = fall_off(x, chance=.05)
    if index != 0:
        return index + len(segment[:primerIndex])
    else:
        return len(segment) - 1

def find_falloff_backward_index_in_segment(segment, primerIndex):
    #Function will find the index where the PCR will fall off
    #First, get the length of the segment up to where the primer starts.
    #Then, calculate the index of the fall off.  Index of 0 means no fall of.
    #If fall off exists, return the index from the fall off.
    #Otherwise, no fall off is found.  So the index will be the first character of the string.
    x = len(segments[:primerIndex])
    index = fall_off_back(x, chance=.05)
    if index != 0:
        return index
    else:
        return 0

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

    dna = ['','']
    dna[0] = gen_dna(args['n'])
    dna[1] = create_compliment(dna[0])

    index_f = random.randint(args['m'] + 1, args['n'] - args['m'] - 1)
    index_b = len(dna[0]) - index_f - 1

    # TODO generate primer
    primer_f = get_primer(dna[0], index_f, args['m'])
    temp_d, temp_i = reverse_strand(dna[1], index_b)
    primer_b = get_primer(temp_d, temp_i, argsp['m'])[::-1]
    del temp_d, temp_i

    segments_f = {(0,-1)}
    segments_b = {(-1,0)}
    # iterate for number of cycles
    for x in xrange(0, args['c']):
        try:
            new_f, new_b = simulate(segments_f, segments_b, primer_f, primer_b)
        except Exception as e:
            print("Errored on cycle %d of %d.\r\nWith error %s." % (x, args['c'], e.message))
            break
        print("-------------------- Cycle %d stats --------------------" % (x))
        num_new_frags = sum(new_f.values()) + sum(new_b.values)
        print("Fragments made: %d" % (num_new_frags))
        print("Average length of fragments made: %f" % (num_new_frags / (len(new_f) + len(new_b))))
        print("New distributions: %s" % (distribution_of_new_segments(new_f, new_b)))

        # TODO merge dictionaries
        segments_f = new_f
        segments_b = new_b

    # print aggregate stats

    pass

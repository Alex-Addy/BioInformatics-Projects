#!/usr/bin/python

from __future__ import print_function
from __future__ import division

import random
# set up random

def fall_off(start, end, failure_chance):
    """Uniform fall off

       Returns a positive integer if the found fall_off is <= size.
       Returns 0 otherwise
    """
    assert abs(start-end) > 1, "start %d end %d" % (start, end)
    assert 1 >= failure_chance >= 0, "Failure chance is outside percent range: %r" % failure_chance
    #len(gene) * (100 / (fall off rate * 100)) == top of range
    if start < end:
        top_range = ((end - start) // failure_chance) + start
        fallen = random.randrange(start, top_range)
        return fallen
    else:
        bot_range = ((end - start) // failure_chance)
        fallen = random.randrange(0-start, bot_range-start, -1)
        return fallen

def multi_find(src, sub):
    '''Returns all found intstances of sub in src'''
    findings = []
    prev = src.find(sub)
    while prev >= 0:
        findings.append(prev)
        prev = src.find(sub, prev+1)
    return findings

def get_primer_i(dna, index, length):
    # Gets the primers for the section to be
    # copied.  Index defines the beginning of the section.

    found = multi_find(dna, dna[index:index+length])
    while len(found) > 1 and index >= 0:
        index -= 1
        found = multi_find(dna, dna[index:index+length])
    if index < 0:
        raise ValueError("Couldn't find a valid primer")
    return found[0]

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
def simulate(strand_norm, strand_prime, primer_f_i, primer_b_i, strand_len, chance=0.05):
    # strandForward is a dictionary containing the forward running strands
    # strandBackward is a dictionary containing the backward running strands
    # primerForward is the piece of dna that the inverse of it would connect to on forward strands
    # primerBackward is the piece of dna that the inverse of it would connect to on backward strands

    #Generate the two temporary dictionaries to hold the new strands
    new_strand_f = {} 
    new_strand_b = {}

    # copy normal strands, become prime strands
    for s in strand_norm:
        # check that primer is contained in strand
        if s[0] <= primer_f_i and primer_f_i + strand_len <= s[1] and \
            abs(s[0]-s[1]) > strand_len:
	    #print(s)
            for _ in xrange(strand_norm[s]):
                falloff = fall_off(s[1], s[0], chance)
                if falloff < s[0]: falloff = s[0]
                new_strand_b[(s[1], falloff)] = new_strand_b.get((s[1], falloff), 0) + 1

    # copy prime strands, become normal strands
    for s in strand_prime:
        if s[0] >= primer_b_i and primer_b_i - strand_len >= s[1] and \
            abs(s[0]-s[1]) > strand_len:
	    #print(s)
            for _ in xrange(strand_prime[s]):
                falloff = fall_off(s[1], s[0], chance)
                if falloff > s[0]: falloff = s[0]
                new_strand_f[(s[1], falloff)] = new_strand_f.get((s[1], falloff), 0) + 1

    #return the two new dictionaries
    return new_strand_f, new_strand_b

def create_compliment(letters):
    #Function will create a compliment of the dna strand string passed in.
    newLetters = letters.replace("A", "K")
    newLetters = newLetters.replace("T", "A")
    newLetters = newLetters.replace("K", "T")

    newLetters = newLetters.replace("C", "K")
    newLetters = newLetters.replace("G", "C")
    newLetters = newLetters.replace("K", "G")

    return newLetters

def distribution_of_segment_lengths(new_f, new_b):
    len2num = {}
    for k, v in new_f.iteritems():
        length = abs(k[0] - k[1])
        if length in len2num:
            len2num[length] += v
        else:
            len2num[length]  = v

    for k, v in new_b.iteritems():
        length = abs(k[0] - k[1])
        if length in len2num:
            len2num[length] += v
        else:
            len2num[length]  = v

    return len2num

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
    index_b = index_f + args['m']

    primer_f_i = get_primer_i(dna[0], index_f, args['m'])
    temp_d, temp_i = reverse_strand(dna[1], index_b)
    primer_b_i =  (args['n'] - 1) - get_primer_i(temp_d, temp_i, args['m'])
    del temp_d, temp_i
    print("P_f_i %d" % (primer_f_i))
    print("P_b_i %d" % (primer_b_i))

    segments_f = {(0,args['n']-1):1}
    segments_b = {(args['n']-1,0):1}
    # iterate for number of cycles
    for x in xrange(0, args['c']):
        chance = 0.001 * (x+1) # gives a chance that starts and stays small
        try:
            new_f, new_b = simulate(segments_f, segments_b, primer_f_i, primer_b_i, args['m'], chance)
        except Exception as e:
            print("Errored on cycle %d of %d.\r\nWith error %s." % (x, args['c'], e.message))
            raise
            break
        print("-------------------- Cycle %d stats --------------------" % (x+1))
        num_new_frags = sum(new_f.values()) + sum(new_b.values())
        print("Fragments made: %d" % (num_new_frags))
        length_created = sum((abs(s[0] - s[1]) for s in new_f)) + sum((abs(s[0] - s[1]) for s in new_b))
        print("Average length of fragments made: %f" % (length_created / num_new_frags))
        #print("New distributions: %s" % (distribution_of_segment_lengths(new_f, new_b)))

        # merge dictionaries
        for k, v in new_f.iteritems():
            segments_f[k] = segments_f.get(k, 0) + v
        for k, v in new_b.iteritems():
            segments_b[k] = segments_b.get(k, 0) + v
        #print('NF', new_f)
        #print('F', segments_f)
        #print('NB', new_b)
        #print('B', segments_b)

    # print aggregate stats
    num_frags = sum(segments_f.values()) + sum(segments_b.values())
    print("Total fragments made: %d" % (num_frags))
    length_created = sum((abs(s[0] - s[1]) for s in segments_f)) + sum((abs(s[0] - s[1]) for s in segments_b))
    print("Average length of fragments made: %f" % (length_created / num_new_frags))
    print("Distribution of lengths: %s" % (distribution_of_segment_lengths(segments_f, segments_b)))

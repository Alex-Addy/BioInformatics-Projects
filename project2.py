from ProteinLookup import *

#test case: aaac agc
#output: _agc


def global_alignment(dna1, dna2):
    dna1 = dna1.lower()
    dna2 = dna2.lower()

    dna1 = ' ' + dna1
    dna2 = ' ' + dna2
    
    lengthTop = len(dna1)
    lengthBot = len(dna2)

    table = [[0 for x in xrange(lengthTop)] for x in xrange(lengthBot)]
    direction = [["" for x in xrange(lengthTop)] for x in xrange(lengthBot)]

    inserts = 0
    deletes = 0

    #setup table
    #1 = left
    #2 = diag
    #3 = up
    #TODO: replace -2 with argument g
    for x in range(0,lengthTop):
        table[0][x] = x * -2
        direction[0][x] = 1
    for y in range(0,lengthBot):
        table[y][0] = y * -2
        direction[y][0] = 3

    #table debug statement
    #print_table(table)

    #calculate values
    for x in range(1,lengthTop):
        for y in range(1,lengthBot):
            up = table[y-1][x] - 2
            left = table[y][x-1] - 2
            if dna1[x] == dna2[y]:
                diag = table[y-1][x-1] + 1
            else:
                diag = table[y-1][x-1] - 1

            #selection process curently favors diagonals
            #if a tie is present
            table[y][x] = diag
            direction[y][x]=2
            if up > table[y][x]:
                table[y][x] = up
                direction[y][x]=3
            if left > table[y][x]:
                table[y][x] = left
                direction[y][x]=1

    #table debug statement
    #print_table(table)
    #print_table(direction)

    #trace back through table
    x = lengthTop - 1
    y = lengthBot - 1

    dnaFinal1 = ""
    dnaFinal2 = ""
    while not (x == 0 and y == 0):

        #match
        if direction[y][x] == 2:
            dnaFinal1 = dna1[x] + dnaFinal1
            dnaFinal2 = dna2[y] + dnaFinal2
            x-=1
            y-=1
            
        #insertion
        elif direction[y][x] == 3:
            dnaFinal1 = "_" + dnaFinal1
            dnaFinal2 = dna2[y] + dnaFinal2
            y-=1
            inserts += 1
            #print "Inserted"

        #deletion
        elif direction[y][x] == 1:
            dnaFinal1 = dna1[x] + dnaFinal1
            dnaFinal2 = "_" + dnaFinal2
            x-=1
            deletes += 1
            #print "Deleted"

    print "Insertions: " + str(inserts)
    print "Deletions: " + str(deletes)

    return(dnaFinal1, dnaFinal2)

def print_table(table):
    for x in range(0, len(table)):
        print table[x]

def check_mutations(dna1, dna2):
    #returns number of syn. and nonsyn. mutations
    syn = 0
    nonsyn = 0
    
    for i in range(0, len(dna1), 3):
        codon1 = dna1[i:i+3]
        codon2 = dna2[i:i+3]
        if codon1 != codon2 and i < len(dna1):
            if get_protein(codon1) != get_protein(codon2):
                syn += 1
            else:
                nonsyn += 1
    return syn, nonsyn

if __name__ == '__main__':
    import argparse
    #TODO: add info
    parser = argparse.ArgumentParser(description="TODO: add info")
    parser.add_argument('m', type=int, help="Scoring for match")
    parser.add_argument('i', type=int, help="Scoring for mismatch")
    parser.add_argument('g', type=int, help="Scoring for gap")

    dna1 = raw_input("Enter the first strand:")
    dna2 = raw_input("Enter the second strand:")

    strand1, strand2 =  global_alignment(dna1, dna2)
    #print strand1 + '\n' + strand2
    syn, nonsyn = check_mutations(strand1, strand2)
    print "Synonymous mutations: " + str(syn)
    print "Nonsynonymous mutations: " + str(nonsyn)

from ProteinLookup import get_protein

#test case: aaac agc
#output: _agc


def global_alignment(dna1, dna2, match_score, mismatch_score, gap_score):
    dna1 = dna1.lower()
    dna2 = dna2.lower()

    dna1 = ' ' + dna1
    dna2 = ' ' + dna2
    
    lengthTop = len(dna1)
    lengthBot = len(dna2)

    table =     [[0  for x in xrange(lengthTop)] for x in xrange(lengthBot)]
    direction = [["" for x in xrange(lengthTop)] for x in xrange(lengthBot)]

    inserts = 0
    deletes = 0

    # setup table
    # 1 = left
    # 2 = diagonal
    # 3 = up
    # TODO: replace -2 with argument g
    for x in range(0,lengthTop):
        table[0][x]     = x * gap_score
        direction[0][x] = 1
    for y in range(0,lengthBot):
        table[y][0]     = y * gap_score
        direction[y][0] = 3

    #table debug statement
    #print_table(table)

    #calculate values
    for x in range(1,lengthTop):
        for y in range(1,lengthBot):
            up = table[y-1][x]   + gap_score
            left = table[y][x-1] + gap_score
            if dna1[x] == dna2[y]:
                diag = table[y-1][x-1] + match_score
            else:
                diag = table[y-1][x-1] + mismatch_score

            #selection process currently favors diagonals
            #if a tie is present
            table[y][x] = diag
            direction[y][x] = 2
            if up > table[y][x]:
                table[y][x]     = up
                direction[y][x] = 3
            if left > table[y][x]:
                table[y][x]     = left
                direction[y][x] = 1

    #table debug statement
    #print_table(table)
    #print_table(direction)
    print "Final score: " + str(table[y][x])
    
    #trace back through table
    x = lengthTop - 1
    y = lengthBot - 1

    dnaFinal1 = []
    dnaFinal2 = []
    while not (x == 0 and y == 0):

        #match
        if direction[y][x] == 2:
            dnaFinal1.append(dna1[x])
            dnaFinal2.append(dna2[y])
            x -= 1
            y -= 1
            
        #insertion
        elif direction[y][x] == 3:
            dnaFinal1.append("_")
            dnaFinal2.append(dna2[y])
            y -= 1
            inserts += 1
            #print "Inserted"

        #deletion
        elif direction[y][x] == 1:
            dnaFinal1.append(dna1[x])
            dnaFinal2.append("_")
            x -= 1
            deletes += 1
            #print "Deleted"

    print "Insertions: " + str(inserts)
    print "Deletions: "  + str(deletes)

    return ''.join(dnaFinal1[::-1]), ''.join(dnaFinal2[::-1])

def print_table(table):
    for x in range(0, len(table)):
        print table[x]

def check_mutations(dna1, dna2):
    '''Returns the number of synonymous and non-synonymous mutations.'''
    # returns number of syn. and non-syn. mutations
    syn = 0
    nonsyn = 0
    
    for i in range(0, len(dna1), 3):
        codon1 = dna1[i:i+3]
        codon2 = dna2[i:i+3]
        if codon1 != codon2 and i <= len(dna1):
            if get_protein(codon1) == '' or get_protein(codon2) == '':
                nonsyn += 1
            elif get_protein(codon1) != get_protein(codon2):
                nonsyn += 1
            else:
                syn += 1
    return syn, nonsyn

def fastaFromFile(open_file):
    assert type(open_file) is file, "Need an open file handle to work"
    cur_gene = ''
    for line in open_file:
        if line[0] == '>':
            if cur_gene == '': continue
            yield cur_gene
            cur_gene = ''
        else:
            cur_gene += line.strip()

def main(f1, f2, m_score, i_score, g_score):
    while True:
        gen1 = fastaFromFile(f1)
        gen2 = fastaFromFile(f2)
        try:
            strand1, strand2 = global_alignment(next(gen1), next(gen2), m_score, i_score, g_score)
        except StopIteration:
            return
        # print strand1
        # print "- - -"
        # print strand2
        strand1 = strand1.upper().replace("T", "U")
        strand2 = strand2.upper().replace("T", "U")
        syn, nonsyn = check_mutations(strand1, strand2)
        print "Synonymous mutations: " + str(syn)
        print "Non-synonymous mutations: " + str(nonsyn)
        print "-------------------------------" * 2

if __name__ == '__main__':
    import argparse
    #TODO: add info
    parser = argparse.ArgumentParser(description="TODO: add info")
    parser.add_argument('m_score', type=int, help="Scoring for match")
    parser.add_argument('i_score', type=int, help="Scoring for mismatch")
    parser.add_argument('g_score', type=int, help="Scoring for gap")

    parser.add_argument('--gene-file-1', type=argparse.FileType('r'), help="File containing the NCBI coding sequences")
    parser.add_argument('--gene-file-2', type=argparse.FileType('r'), help="File containing the NCBI coding sequences")

    args = vars(parser.parse_args())

    main(args["gene-file-1"], args["gene-file-2"], args["m_score"], args["i_score"], args["g_score"])


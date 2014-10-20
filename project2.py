from ProteinLookup import get_protein

#test case: aaac agc
#output: _agc


def global_alignment(dna1, dna2, match_score, mismatch_score, gap_score):
    """ Finds the best global alignment for the two given strings.
    
        Returns a 5-tuple of items:
        aligned dna1, aligned dna2, insertions, deletions, final score
    """
    dna1 = dna1.upper()
    dna2 = dna2.upper()

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
    #print "Final score: " + str(table[y][x])
    
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

    #print "Insertions: " + str(inserts)
    #print "Deletions: "  + str(deletes)

    #print "%d,%d" % (inserts, deletes)

    return ''.join(dnaFinal1[::-1]), ''.join(dnaFinal2[::-1]), inserts, deletes, table[lengthBot-1][lengthTop-1]

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
    """Takes an open file handle, and returns a list of genes.
    
        Assumes that genes are seperated by a line starting with a '>'.
    """
    assert type(open_file) is file, "Need an open file handle to work"
    genes = []
    cur_gene = ''
    for line in open_file:
        if line[0] == '>':
            if cur_gene == '': continue
            genes.append(cur_gene.upper())
            cur_gene = ''
        else:
            cur_gene += line.strip()
    genes.append(cur_gene.upper())
    return genes

def main(f1, f2, m_score, i_score, g_score):
    gene_list_1 = fastaFromFile(f1)
    gene_list_2 = fastaFromFile(f2)

    # sudan strand is missing the eighth gene, so we advance the other side past it to the next gene
    if "Sudan1976.txt" in f1.name:
        gene_list_1.insert(-1, '')
    elif "Sudan1976.txt" in f2.name:
        gene_list_2.insert(-1, '')

    for gene_num in range(0, len(gene_list_1)):
        if gene_list_1[gene_num] == '' or gene_list_2[gene_num] == '':
            #print "Empty gene %d with genes:" % (gene_num)
            #print "\t%s" % (gene_list_1[gene_num])
            #print "\t%s" % (gene_list_2[gene_num])
            #print ""
            continue

        strand1, strand2 = gene_list_1[gene_num], gene_list_2[gene_num]
        #print "Gene #%d with files '%s' and '%s'" % (gene_num, f1.name, f2.name)
        strand1, strand2, insertions, deletions, final_score = global_alignment(strand1, strand2, m_score, i_score, g_score)
        #print strand1
        #print strand2

        # print strand1
        # print "- - -"
        # print strand2
        strand1 = strand1.upper().replace("T", "U")
        strand2 = strand2.upper().replace("T", "U")
        syn, nonsyn = check_mutations(strand1, strand2)
        print "%s,%d,%d,%d,%d,%d,%d" % (f2.name, gene_num+1, insertions, deletions, syn, nonsyn, final_score)
        #print "Synonymous mutations: %d" % (syn)
        #print "Non-synonymous mutations: %d" % (nonsyn)
        #print "="*40
        #print ''

if __name__ == '__main__':
    import argparse
    #TODO: add info
    parser = argparse.ArgumentParser(description="TODO: add info")
    parser.add_argument('m_score', type=int, help="Scoring for match")
    parser.add_argument('i_score', type=int, help="Scoring for mismatch")
    parser.add_argument('g_score', type=int, help="Scoring for gap")

    args = vars(parser.parse_args())

    km_files = \
    ["KM233118.txt", "KM233040.txt", "KM233041.txt", "KM233042.txt", "KM233043.txt", "KM233044.txt", "KM233045.txt", "KM233046.txt",
        "KM233047.txt", "KM233048.txt", "KM233049.txt", "KM233050.txt", "KM233051.txt", "KM233052.txt", "KM233053.txt", "KM233054.txt",
        "KM233055.txt", "KM233056.txt", "KM233057.txt", "KM233058.txt", "KM233059.txt", "KM233060.txt", "KM233061.txt", "KM233062.txt",
        "KM233063.txt", "KM233064.txt", "KM233065.txt", "KM233066.txt", "KM233067.txt", "KM233068.txt", "KM233069.txt", "KM233070.txt",
        "KM233071.txt", "KM233072.txt", "KM233073.txt", "KM233074.txt", "KM233075.txt", "KM233076.txt", "KM233077.txt", "KM233078.txt",
        "KM233079.txt", "KM233080.txt", "KM233081.txt", "KM233082.txt", "KM233083.txt", "KM233084.txt", "KM233085.txt", "KM233086.txt",
        "KM233087.txt", "KM233088.txt", "KM233089.txt", "KM233090.txt", "KM233091.txt", "KM233092.txt", "KM233093.txt", "KM233094.txt",
        "KM233095.txt", "KM233096.txt", "KM233097.txt", "KM233098.txt", "KM233099.txt", "KM233100.txt", "KM233101.txt", "KM233102.txt",
        "KM233103.txt", "KM233104.txt", "KM233105.txt", "KM233106.txt", "KM233107.txt", "KM233108.txt", "KM233109.txt", "KM233110.txt",
        "KM233111.txt", "KM233112.txt", "KM233113.txt", "KM233114.txt", "KM233115.txt", "KM233116.txt", "KM233117.txt"]

    with open("Sudan1976.txt") as sudan_f:
        print "Sudan Ebolavirus,Gene #,Insertion,Deletion,Synonymous Mutations,Nonsynonymous Mutations,Final Score"
        for f_name in km_files:
            with open(f_name) as km_file:
                main(sudan_f, km_file, args["m_score"], args["i_score"], args["g_score"])
            sudan_f.seek(0)

    print ",,,,,,"
    with open("Zaire1976.txt") as zaire_f:
        print "Zaire Ebolavirus,Gene #,Insertion,Deletion,Synonymous Mutations,Nonsynonymous Mutations,Final Score"
        for f_name in km_files:
            with open(f_name) as km_file:
                main(zaire_f, km_file, args["m_score"], args["i_score"], args["g_score"])
            zaire_f.seek(0)

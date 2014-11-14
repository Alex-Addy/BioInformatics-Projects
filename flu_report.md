Bioinformatics Flu Project
--------------------------
#####By: Alex Addy, Nick Thompson, Cory Sutyak

Abstract:

This report focused on studying this seasons flu strands with respect to the ones in this years flu vaccine: A/California/7/2009 (H1N1)pdm09, A/Texas/50/2012 (H3N2), and B/Massachusetts/2/2012. Using resources on the web, we will identify the relationship of the isolates stated above within the past 5 years.

Introduction:

There are key differences between these 3 types of flu.  The A class of influenza viruses are divided into subtypes based on two proteins on the surface of the virus.  Those proteins being hemagglutinin (H) and neuraminidase (N).  Of that, there are 18 types of H and N. (H1 through H18 and N1 through N11).  As implied, that is where the classifications of A types are named.

On the contrary, B class is not divided into subtypes, but they can be broken further down into strains and strains.  The current circulating B class belong of one or two lineages, B/Yamagata and B/Victoria.

(source cdc.gov/flu)

Materials and Methods:
Our data will come from the flu database at NCBI.  Our observations and comparisons will be obtained from using the various tools using the database.  With those tools, we will use a few different algorithms such as neighbor-joining and UPGMA. 

Implementation:
Neighbor Joining is a clustering method to create phylogenetic trees.  To use this algorithm, we need the distance between each pair of sequences.  Generally, the algorithm takes the distances and starts with a completely unresolved tree.  From there it will iterate over a set of steps until the tree is resolved and all branch lengths are known.  First it creates a matrix off of the input.  Then it finds the smallest distance between the input and joins them together.  Then it calculates the distance from each of the inputs to the new node.  Updates the rest of the distances and then starts over.

UPGMA is another clustering method, used to create phenetic trees.  It is most often used to produce guide trees for sophisticated phylogenetic reconstruction algorithms.  It constructs a rooted tree that reflects the structure present in a pairwise similarity matrix.  The algorithm takes the nearest two clusters it knows and combines them into a higher-level cluster.  The distance between those clusters id the average of all distances between pairs of objects in A and B, in other words, the mean distance between elements in a cluster.

(source wikipedia.org)

 Results and discussion:
  1. Questions
      a. There are three flu variants A, B, and C.

      b. Seven possible host species that are considered in the NCBI(\[1\])[1] database : Avian, Bat, Blow Fly, Bovine, Camel, Cat, Ferret.

      c. Both virus types contain 8 nucleotide segments listed as such:
          A; 8 (PB2, PB1, PA/PA-, HA, NP, NA, MP, NS)
          B; 8 (PB1, PB2, PA, HA, NP, NA, MP, NS)

      d. The subtypes H and N stand for hemagglutinin and neuraminidase, respectively. The numbers are the specific subtype of that protein, with there being 18 different H subtypes and 11 different N subtypes(\[2\])[2].

      e. Type A can travel through non-human hosts and is generally responsible for the large flu epidemics. Type B is found only in humans and is typically less severe.(\[3\])[3]

      f. The dominant strands of the flu change from year to year, meaning the immunity gained last year does not apply this year.

  2. How many full length unique nucleotide sequences of H1N1 and H3N2 isolated from people in USA from 1/1/2009 to 10/1/2014 has the database collected? How many of these collected this year?

  |                       | H1N1 | H3N2 | B virus |
  | --------------------- | ---- | -----| ------- |
  | 1/1/2009 to 10/1/2014 | 7850 | 6675 |   1799  |
  | This year             |  670 |  478 |    196  |

  3. Influenza Virus Sequence Tree. Considering unique full length protein sequences coding HA proteins in this year's H1N1 flu viruses infected people in USA, build your influenza virus sequence tree using the neighbor-joining algorithm. What does the tree look like?
    The tree is very flat with most sequences being only a few levels deep.

  4. What distance did you use in part 3? Change your distance measure; how much did your tree change? What's your explanation about the difference? What can you tell your friends about this years H1N1 virus based on your trees?
    F84
    The tree had only minor changes with only a few sequences moving. The movement was mainly in having two neighbor leaf nodes swap places, a minor negligible change
    It is very similar across the board and you should be fine after getting the flu shot.

  5. Repeat part 3 and 4 for H3N2 virus using the UPGMA algorithm.  This tree is deeper showing many subtrees.  Once again changing the distance only results in minor changes.

  6. Repeat part 3 and 4 for combined sequences for H1N1 and H3N2 using neighbor-joining algorithm.  The tree is very one sided with the H1N1 and H3N2 strains being grouped together
	in subtrees.  The change in difference showed little to no change in the resulting tree.

  7. What additional observations have you made from the tree obtained in part 6?  
	The two different strands did not show close similarities.  
    
  Conclusion:
We were tasked with comparing a few different strands of the flu virus.  Of the 3 different types of flu virus, we looked at two strands of A and one of B.  There are a few things to note as a result.  Changing the distance measure for our experiments hardly had any impact on the results.  It would appear the the H3N2 virus is more adaptable than the H1N1 as the tree for it was deeper.  It is a little bit ironic that the non-human found strains are much more of a hazard then the strains found in humans. 
  
  References:
  [1]: http://www.ncbi.nlm.nih.gov/genomes/FLU/aboutdatabase.html
  [2]: http://www.cdc.gov/flu/about/viruses/types.htm
  [3]: http://www.webmd.com/cold-and-flu/flu-guide/advanced-reading-types-of-flu-viruses
  [4]: http://www.wikipedia.org/UPGMA
  [5]: http://www.wikipedia.org/Neighbor_Joining

  
# Introduction  
A Python implementation of a de novo genome assembler based on de Bruijn graphs. Sequencing reads are broken into k-mers, which become the edges of a directed graph whose nodes are (k-1)-mers. Walking an Eulerian path through the graph reconstructs the underlying sequence as one or more contigs.

This assembler is developed on a toy dataset then tested againt the reference genome of *Sacchromyces cerevisiae* with single-end reads, up to 30x coverage.

`DeBruijnGraph` class takes a list of reads and a k-mer size, builds tha graph using recursion and assembles the contigs.

# Pseudocode  
```
CLASS DeBruijnGraph

  INITIALIZE with reads and k:
    create empty graph and store k
    call build_graph_from_reads(reads, k)

  METHOD add_edge(left, right):
    append right to graph[left]

  METHOD remove_edge(left, right):
    remove right from graph[left]

  METHOD build_graph_from_reads(reads, k):
    FOR each k-mer in each read:
      left = first k-1 bases
      right = last k-1 bases
      IF edge does not already exist:
        call add_edge(left, right)

  METHOD eulerian_walk(node, graph, seed, rng, walk):
    initialize rng and walk if needed
    WHILE node has outgoing edges:
      randomly select and remove an edge
      recurse from its destination using the same rng and walk
    append node to walk
    RETURN walk

  METHOD walk_helper(start, graph_copy, rng):
    get and reverse the Eulerian walk
    split wherever consecutive nodes lack an edge
    convert pieces to sequences and return them

  METHOD assemble_contigs(seed):
    initialize rng and copy graph
    count incoming and outgoing edges
    find starts with one extra outgoing edge

    FOR each start, then each remaining node:
      IF it has unused outgoing edges:
        collect contigs from walk_helper

    FOR each contig, longest first:
      hash k-mers using a shared representation for both orientations
      IF contig has k-mers and less than 90% are already seen:
        keep contig and update seen hashes

    RETURN kept contigs

  METHOD tour_to_sequence(tour):
    IF tour is empty:
      RETURN empty string
    join first node with the last base of each remaining node
    RETURN sequence

  METHOD get_assembly_stats(contigs):
    calculate count, total, longest, shortest, and mean length
    accumulate lengths, longest first, to half the total for N50
    RETURN statistics

  METHOD write_fasta(contigs, filename):
    FOR each contig:
      write FASTA header and sequence
```

# Yeast Assembly Results
We ran the assembler on 2,414,266 simulated, error-free 150 bp reads from the *S. cerevisiae* R64 genome using `k=31`. Estimated sequencing coverage was 30×.

| Statistic | Result |
|---|---:|
| Graph nodes | 22,950,037 |
| Distinct graph edges | 22,957,882 |
| Number of contigs | 4,237 |
| Total assembly length | 12,407,104 bp |
| Reference genome size | 12,071,326 bp |
| Assembly length / reference length | 102.78% |
| Longest contig | 136,697 bp |
| Shortest contig | 31 bp |
| Mean contig length | 2,928.3 bp |
| N50 | 26,967 bp |
| Total runtime, excluding file output | 4.15 minutes |

[Full assembly statistics](genome_assembly_stats.txt)

# Successes
We have successfully created the De Bruijn Graph using the build graph function with no errors as far as we can tell. The toy data is correctly assembled using the current function. On the yeast data, the assembly vs genome % is close to 100%. All of these are signs of success in this project. As you will see below, this did not result in connected contigs which means that there is still work to be done to improve the codes output.

# Struggles
The biggest challenge we experienced in this project was the deduplication of reverse strand sequence without removing repeats from the sequence. We had to go through hoops to make sure that the code does not build contigs containing both reverse strand and forward strand sequences at the same time. This resulted in "fragmented" contigs that you can see in the yeast genome. The N50 value is too low to consider this a good assembly. We were able to bring the assembly vs genome % down to almost 100% percent at the cost of a connected graph which makes me think that there is a better way to assemble the genome and get a complete assembly.

# Personal Reflections

**Group Leader: Ahmed Salman**  
The big task this time was to create a good assembly from yeast sequences. I ran into issues while trying to figure out the difference between repeats in a sequence and reverse strand duplicates. Specifically how to make the code tell the difference between the two. While we attempted to clear duplicate contigs after contig assembly, this does not mean that the contig itself was assembled correctly without reverse and forward strands meshing together. It is very possible to create a contig that seems unique but is actually formed from some forward and some reverse strand sequences. Resulting in a contig that shouldn't exist. A possible fix would be to check for reverse complementarity before contig assembly starts. I also want to point out that I do not think recursion is important or necessary in any shape or form here. If anything it made it much harder to control the output of the function without causing downstream problems.

**Other member: Selin Uenal**  
I had learned about de Bruijn graphs conceptually in previous classes, but I had never implemented one before. This project helped me connect the concepts to the code, and I also became more comfortable with classes, object-oriented programming, and recursion. One of the most challenging parts for me and the rest of our group was understanding why our original assembly was almost 2x the reference genome's length and how using reads from both strands could be contributing to that. I learned that we can’t just discard the reverse complement reads, since reads from both strands provide useful information and help cover different portions of the genome. The main challenge is figuring out how to use that information without counting the same regions twice. If we had more time, I would definitely want to dig into that part more deeply.  

**Other Member: Margaret Wenger**  


# Generative AI Appendix
Claude AI (Sonnet 5.5) was used to help make sure our pseudocode matched our code at the end of the project, since our code changed from our initial psueodcode. After finalizing our code, we went back and rewrote parts of the pseudocode, then gave Claude our updated pseudocode and finalized `DeBruijnGraph` Class and asked: "Does our pseusocode match our finalized code?". The output told us it mostly matched, with minor fixes, which were reviewed before adding to the final README.
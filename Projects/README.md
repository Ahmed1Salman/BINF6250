Introduction
A Python implementation of a de novo genome assembler based on de Bruijn graphs. Sequencing reads are broken into k-mers, which become the edges of a directed graph whose nodes are (k-1)-mers. Walking an Eulerian path through the graph reconstructs the underlying sequence as one or more contigs.

This assembler is developed on a toy dataset then tested againt the reference genome of *Sacchromyces cerevisiae* with single-end reads, up to 30x coverage.

`DeBrujGraph` class takes a list of reads and a k-mer size, builds tha graph using recursion and assembles the contigs.

Pseudocode
```
CLASS DeBruijnGraph
  initialize with graph, k, and build_graph_from_reads attributes
  def method add_edge(self_left_right):
    append right to the list of self.graph[left]
    
  def method remove_edge(self,right,left)
    remove right from list of self.graph[left]
    
  def method build_graph_from_reads(self,read,k)
    loop through sequences
      loop through each sequence - k + 1
        prefix = read[i:i+k-1]
        suffix = read[i-1:i+k]
        if edge doe not exist:
          add_edge(prefix, suffix)
  def eulerian_walk(self,node,graph,seed=None)
    initialize kmer_history and walk if None
    initialize kmer_walkback
    if list > 0 then:
      find next node randomly
      append next node to kmer_history
      remove next node from graph
    else:
      walk backwards through kmer_history
      if graph list is empty, append kmer into walk
      else kmer_walkback = i
    return eulerian_walk(node = kmer_walkback, graph = graph, seed = seed)
```
Successes


Struggles
The biggest challenge we experienced in this project was the deduplication of reverse strand sequence without removing repeats from the sequence. We had to go through hoops to make sure that the code does not build contigs containing both reverse strand and forward strand sequences at the same time. This resulted in "fragmented" contigs that you can see in the yeast genome. The N50 value is too low to consider this a good assembly. We were able to bring the assembly vs genome % down to almost 100% percent at the cost of a connected graph which makes me think that there is a better way to assemble the genome and get a complete assembly.

Personal Reflections
Group Leader - Ahmed Salman
The big task this time was to create a good assembly from yeast sequences. I ran into issues while trying to figure out the difference between repeats in a sequence and reverse strand duplicates. Specifically how to make the code tell the difference between the two. While we attempted to clear duplicate contigs after contig assembly, this does not mean that the contig itself was assembled correctly without reverse and forward strands meshing together. It is very possible to create a contig that seems unique but is actually formed from some forward and some reverse strand sequences. Resulting in a contig that shouldn't exist. A possible fix would be to check for reverse complementarity before contig assembly starts.
Other members


Generative AI Appendix
Generative AI was not used for this project.

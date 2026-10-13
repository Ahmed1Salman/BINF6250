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


Personal Reflections
Group Leader


Other members


Generative AI Appendix
Generative AI was not used for this project.

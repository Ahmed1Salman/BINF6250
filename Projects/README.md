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
  def assemble_contigs(self, seed=None):
    set random seed
    make deep copy of graph
    set outdegree_counter (edges leaving node)
    set indegree_counter (incoming edges to node)
    loop through current and forward nodes in graph_copy:
        outdegree_counter[current_node] += number of nodes in forward_nodes
        for each forward_node in forward_nodes:
          indegree_counter[forward_node] += 1
    eularian_start = each node in graph_copy where outdegree = indegree == 1
    initialize contigs list
    #start node exists:
    for each start in eularian_start:
        walk = eularian_walk(start, graph_copy, seed)
        reverse walk
        seq = tour_to_sequence(walk)
        append seq to contig list
    # no defined start node (can start anywhere)
    if all nodes have outdegree - indegree == 0
        start = random node from graph_copy
        walk = eularian_walk(start, graph_copy, seed)
        reverse walk
        seq = tour_to_sequence(walk)
        append seq to contig list
    return contig list
  def tour_to_sequence(self, tour):
    if tour is empty or None:
        return ""
    sequence = first k-1mer
    for each kmer in tour [:1]:
      sequence =+ last character of kmer
    return sequence
  def get_assembly_stats(self, contigs):
    initialize dict for stats storing
    num_contigs = length of contigs list
    contig_length = length of each contig
    total_length = sum of all contig_lengths
    longest_contig = max of contig_length
    shortest_contig = min of contig_length
    mean_length = contig_length / num_contig
    n50_threshold = total_length / 2
    n50_sum = 0
    for each length in lengths, reverse sorted:
      n50_sum += length of contig
      if sum > threshold: # dont want to exceed threshold
        n50_sum = length
        break
    return stats
  def write_fasta(self, contigs, filename):
    open filename for writing
    for each (number, contig) in contigs:
      write ">contig_" + number + newline
      write contig + newline
```
Successes


Struggles


Personal Reflections
Group Leader


Other members


Generative AI Appendix
Generative AI was not used for this project.

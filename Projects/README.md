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
        if edge is not in graph[prefix]:
          add_edge(prefix, suffix)

  def eulerian_walk(self,node,graph,seed=None, rng=None, walk=None):
    initialize rng and walk if None already exist. Do not reset if there are values already

    while graph[node] is not empty:
        pick a random edge from graph[node]
        remove it from graph[node] 
        eulerian_walk(chosen_path, graph, seed, rng, walk) # this is where recursion happens

    Append node to walk
    Return walk

  def walk_helper(start, graph_copy, rng):
    walk = eulerian_walk(start, graph_copy, rng)
    reverse walk as it wasn't reversed in eulerian_walk
    out = empty list
    piece = [walk[0]] #first kmer in walk
    FOR each consecutive pair (a, b) in walk:
        IF edge a to b does NOT exist in the ORIGINAL graph:
          append tour_to_sequence(piece) to contigs
            piece = empty list
        append b to piece
    append tour_to_sequence(piece) to contigs
    RETURN contigs

  def assemble_contigs(seed):
    rng = new random generator(seed)
    graph_copy = copy of graph #to prevent destruction of graph
    #Count indegrees and outdegrees
    FOR each node, forward nodes in graph_copy:
        outdegree[node] += len(neighbors)
        FOR each neighbor: indegree[neighbor] += 1

  eulerian_starts is nodes where outdegree − indegree == 1
  
  FOR each start in starts:
        IF graph_copy[start] is empty: CONTINUE
        contigs += walk_helper(start, graph_copy, rng)

  #Same operation performed on remaning nodes as they dont have a eulerian start
  FOR each node in graph_copy:
        IF graph_copy[node] is empty: CONTINUE
        contigs += walk_helper(node, graph_copy, rng)

  #Check for reverse complementarity and remove similar contigs to prevent duplication
    complement ← table to calculate reverse compliment
    seen = empty set and  kept = empty list
    FOR each contig in contigs sorted by length, longest first:
        hashes = empty list
        FOR each k-mer in contig:
            canonical ← MIN(k-mer, reverse_complement(k-mer))
            append hash(canonical) to hashes
        IF hashes not empty AND fraction of hashes already in seen < 0.9:
            append contig to kept
            add all hashes to seen
    RETURN kept

  def tour_to_sequence(tour):
      IF tour is empty: RETURN empty string
      else RETURN first node + last character of each remaining node in tour

  def get_assembly_stats(contigs):
      lengths = length of each contig
      num_contigs = count
      total_length = SUM(lengths)
      longest = MAX(lengths);  shortest ← MIN(lengths)
      mean_length = total_length / num_contigs

      threshold = total_length / 2
      current_tally = 0
      FOR each contig sorted longest first:
          running += length(contig)
          IF running ≥ threshold:
              n50 ← length(contig) and stop the code, else continue
      RETURN all stats #NOTE: all stats are stored as keys in the dictionary named stats

  def write_fasta(contigs, filename):
      open filename for writing
      FOR each contig with index n:
          write ">contig_n" then the sequence on the next line
      #This causes one line to contain the contig number and the next line contain the sequence
```
Successes
We have successfully created the De Bruijn Graph using the build graph function with no errors as far as we can tell. The toy data is correctly assembled using the current function. On the yeast data, the assembly vs genome % is close to 100%. All of these are signs of success in this project. As you will see below, this did not result in connected contigs which means that there is still work to be done to improve the codes output.

Struggles
The biggest challenge we experienced in this project was the deduplication of reverse strand sequence without removing repeats from the sequence. We had to go through hoops to make sure that the code does not build contigs containing both reverse strand and forward strand sequences at the same time. This resulted in "fragmented" contigs that you can see in the yeast genome. The N50 value is too low to consider this a good assembly. We were able to bring the assembly vs genome % down to almost 100% percent at the cost of a connected graph which makes me think that there is a better way to assemble the genome and get a complete assembly.

Personal Reflections
Group Leader - Ahmed Salman
The big task this time was to create a good assembly from yeast sequences. I ran into issues while trying to figure out the difference between repeats in a sequence and reverse strand duplicates. Specifically how to make the code tell the difference between the two. While we attempted to clear duplicate contigs after contig assembly, this does not mean that the contig itself was assembled correctly without reverse and forward strands meshing together. It is very possible to create a contig that seems unique but is actually formed from some forward and some reverse strand sequences. Resulting in a contig that shouldn't exist. A possible fix would be to check for reverse complementarity before contig assembly starts. I also want to point out that I do not think recursion is important or necessary in any shape or form here. If anything it made it much harder to control the output of the function without causing downstream problems.
Other members


Generative AI Appendix
Claude AI (Sonnet 5.5) was used to help create the pseudocode for this README file. Claude was fed the full code file and asked: "Can you create pseudocode for the De Bruijn graph class only?". Output was checked and revised before usage.

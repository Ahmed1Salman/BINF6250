# Introduction
Description of the project

# Pseudocode
Put pseudocode in this box:

```
Some pseudocode here
```

# Successes
Description of the team's learning points

# Struggles
Description of the stumbling blocks the team experienced

# Personal Reflections
## Group Leader
Group leader's reflection on the project

## Other member
Other members' reflections on the project

# Generative AI Appendix
After we created a skeleton code for the `GibbsMotifFinder()` function, we kept getting errors due to a negative probability. I put this prompt into Claude with the whole function we had written "I am working on this function that finds a pfm from a list of strings using a Gibbs sampler and am receiving a negative probabilities error. I know this has to do with the log2 conversions, but can you help me understand what parts of this code need to be fixed?" Claude brought to our attention a couple of other bugs that we then worked on. It told us that the cause of the error was that the log-odds scores were used as weights, so we had to undo the log before sampling by doing `2 ** score`. It also helped us understand that our original function had `random.choices()` returning the chosen index but not storing it, so we had to create a variable that did that. Furthermore, it pointed out a bigger problem, which was that our code was building the PFM from the `seqs` themselves rather than from the k-mers, and it had a `current_pos` that was shared by all the sequences. It pointed out a minor problem with our original `seqs[randint][current_pos+index : k+index]` which has length `k-current_pos` not `k`. It helped me understand that our `rng.integers(0, len(seqs) - 1)` couldn't actually pick the last sequence, so that had to be fixed, and that our `for seq in seqs` line ran only 'len(seqs)' updates so `seq` wasn't used. This is a problem because Gibbs samplers need many iterations or a loop that runs until the motif stops changing, and the instructions for the project say to run until 10,000. Finally, it pointed out that we seeded both `random` and  `np.random` but we were supposed to use `rng`. Claude's suggestions were helpful to get past where the program got stuck and understand what changes had to be made.

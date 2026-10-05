# Introduction
This project implements a Gibbs Sampler for motif discovery in DNA. As a MCMC algorithm, the Gibbs Sampler searches for motifs from random positions in DNA sequences, and refines them over time until convergence is achieved (or the 10000 loop limit is reached in this code). The function `GibbsMotifFinder(seqs, k, seed=None)` takes a list of DNA sequences and a motif length k and returns a 4 x k position frequency matrix (PFM). This algorithm assumes that we know the length of the expected motif (k) and that every sequence contains the motif. The algorithm waws tested on B. subtilis promoters and nrf1 chip-seq data. The final pfm was visualized using a sequence logo (seqlogo).

# Pseudocode
Put pseudocode in this box:

```
GibbsMotifFinder(seqs, k, seed = None)
    SET random seeds (random and numpy) using seed
    CONVERT every sequence in seqs to uppercase
    INITIALIZE motif empty list

    # Initialization
    for each sequence in seqs
        start <- random integer in [0, length(sequence) - k]
        append sequence[start : start + k] to motifs

    unchanged <- 0

    # Iterative refinement
    for j in (1 to 10000)
        i <- random integer in [0, number of sequences - 1]
        motifs_excluded <- motifs with motif i removed

        PFM <- build_pfm(motifs_excluded, k)
        PWM <- build_pwm(PFM)       

        candidates <- empty list
        scores <- empty list
        for each position p from 0 to length(seqs[i]) - k + 1
            kmer <- seqs[i][p : p + k]
            for each candidate in (kmer, reverse_complement(kmer))
                append candidate to candidates
                append score_kmer(candidate, PWM) to scores

        weights <- [2 ^ s for each s in scores]    # log2 score -> positive weight
        new_motif <- random choice from candidates, with probability
                     proportional to weights    # P(m) = A_m / sum(A_l)

        if new_motif == motifs[i]
            unchanged <- unchanged + 1
        else
            unchanged <- 0
        motifs[i] <- new_motif

        if j is a multiple of 1000
            print iteration, information content of PFM, elapsed time in seconds

        if unchanged >= 200
            break                                # motifs have converged

    PFM_final <- build_pfm(motifs, k)
    return PFM_final
```

# Successes
Understanding the Gibbs Sampling algorithm from top to bottom: We spent a lot of time together trying to understand the algorithm before we even started programming anything. Then we spent even more time reading the python files accompanying the notebook that contained the helper functions. Understanding the functions was important before we start work on the algorithm. Once we understood the algorithm and the helper functions, programming a prototype was much faster, We were able to break down its steps to leaving out one sequence, building a PFM, then scoring the sequence, then choose a different starting point and repeat. We did have to figure out how to solve some problems such as the negative weight problem and the log2 transformation. We successfully tested the algorithm using the B. subtilis promoters and found the Shine-Dalgarno motif.

# Struggles
During the entire project, we had trouble contacting our third team mate. We (Ahmed Salman and Katelyn Dsouza) met together and worked on the project. During the 2 weeks duration, we messaged our third partner on Teams many times and we proceeded to email them using their Northeastern Email with no success. Beyond team trouble, running the code using the nrf1 data produced almost no results. The information content was too low by the time the 10000 loop limit was reached, I believe that increasing that limit significantly would provide a reasonable results but it would take much time to do. The algorithm as it stands takes 2 hours to finish (12 minutes per 1000 loops) and increasing the limit linearly increases the time required to finish the algorithm. Also, as discussed above, negative probabilities created problems as the `random.choice` function do not accept log2 or negative probabilities. 

# Personal Reflections
## Group Leader
Ahmed Salman - The hardest part of this project was understanding the algorithm, the supporting functions, and how they are supposed to interact together. We spent more than a day to understand all of that. The implementation of the code was quicker once our understanding of the project. Honestly, I can't think of a better way to learn an algorithm inside out better than implementing it from the ground up. Coding is like trying to explain complicated algorithms to a 5 year old that can only do exactly as asked. On a side note, as stated above running the nrf1 file into the function produces nearly no data so I had the idea to try and increase the loop limit so that I can make the code run longer with the goal of identifying at what loop does the code finally "catch" the expected sequence. I am not expecting the code the fully execute, I am just attempting to see how far our algorithm can go until it finds the sequence in question.

## Other member
Other members' reflections on the project

# Generative AI Appendix
After we created a skeleton code for the `GibbsMotifFinder()` function, we kept getting errors due to a negative probability. I put this prompt into Claude with the whole function we had written "I am working on this function that finds a pfm from a list of strings using a Gibbs sampler and am receiving a negative probabilities error. I know this has to do with the log2 conversions, but can you help me understand what parts of this code need to be fixed?" Claude brought to our attention a couple of other bugs that we then worked on. It told us that the cause of the error was that the log-odds scores were used as weights, so we had to undo the log before sampling by doing `2 ** score`. It also helped us understand that our original function had `random.choices()` returning the chosen index but not storing it, so we had to create a variable that did that. Furthermore, it pointed out a bigger problem, which was that our code was building the PFM from the `seqs` themselves rather than from the k-mers, and it had a `current_pos` that was shared by all the sequences. It pointed out a minor problem with our original `seqs[randint][current_pos+index : k+index]` which has length `k-current_pos` not `k`. It helped me understand that our `rng.integers(0, len(seqs) - 1)` couldn't actually pick the last sequence, so that had to be fixed, and that our `for seq in seqs` line ran only 'len(seqs)' updates so `seq` wasn't used. This is a problem because Gibbs samplers need many iterations or a loop that runs until the motif stops changing, and the instructions for the project say to run until 10,000. Finally, it pointed out that we seeded both `random` and  `np.random` but we were supposed to use `rng`. Claude's suggestions were helpful to get past where the program got stuck and understand what changes had to be made.

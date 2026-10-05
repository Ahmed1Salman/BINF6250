# Introduction
This project implements a Gibbs Sampler for motif discovery in DNA. As a MCMC algorithm, the Gibbs Sampler searches for motifs from random positions in DNA sequences, and refines them over time until convergence is achieved (or the 10000 loop limit is reached in this code). The function `GibbsMotifFinder(seqs, k, seed=None)` takes a list of DNA sequences and a motif length k and returns a 4 x k position frequency matrix (PFM). This algorithm assumes that we know the length of the expected motif (k) and that every sequence contains the motif. The algorithm waws tested on B. subtilis promoters and nrf1 chip-seq data. The final pfm was visualized using a sequence logo (seqlogo).

# Pseudocode

```
GibbsMotifFinder(seqs, k, seed = None)
    SET random seeds (random and numpy) using seed
    CONVERT every sequence in seqs to uppercase
    INITIALIZE motifs empty list

    # Initialization
    for each sequence in seqs
        start <- random integer in [0, length(sequence) - k]
        append sequence[start : start + k] to motifs

    PFM_total <- build_pfm(motifs, k)
    unchanged <- 0

    # Iterative refinement
    for j in (1 to 10000)
        i <- random integer in [0, number of sequences - 1]
        old_motif <- motifs[i]

        PFM_excluded <- PFM_total - build_pfm([old_motif], k)
        PWM <- build_pwm(PFM_excluded)       

        if j is a multiple of 1000
            print iteration, information content of PFM, elapsed time in seconds

        candidates <- empty list
        scores <- empty list
        for each position p from 0 to length(seqs[i]) - k
            kmer <- seqs[i][p : p + k]
            if kmer contains 'N'
                skip to next position
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
            PFM_total <- PFM_excluded + build_pfm([new_motif], k) #add new motif's counts
        motifs[i] <- new_motif

        if unchanged >= 200
            break                                # motifs have converged

    PFM_final <- build_pfm(motifs, k)
    return PFM_final
```

# Successes
Understanding the Gibbs Sampling algorithm from top to bottom: We spent a lot of time together trying to understand the algorithm before we even started programming anything. Then we spent even more time reading the python files accompanying the notebook that contained the helper functions. Understanding the functions was important before we start work on the algorithm. Once we understood the algorithm and the helper functions, programming a prototype was much faster, We were able to break down its steps to leaving out one sequence, building a PFM, then scoring the sequence, then choose a different starting point and repeat. We did have to figure out how to solve some problems such as the negative weight problem and the log2 transformation. We successfully tested the algorithm using the B. subtilis promoters and found the Shine-Dalgarno motif.

# Struggles
During the entire project, we had trouble contacting our third team mate. We (Ahmed Salman and Katelyn DSouza) met together and worked on the project. During the 2 weeks duration, we messaged our third partner on Teams many times and we proceeded to email them using their Northeastern Email with no success. Beyond team trouble, running the code using the nrf1 data produced almost no results. Our first version of the algorithm rebuilt the PFM from every motif in the every round, which took about 2 hours for the full 10,000 loop limit. We had to change this to build the PFM once before the loop and then subtract or add the counts for the one motif that changed every round. This brought the run time down significantly to just a few seconds. Even this faster version produced a low information content since each round updates one sequence, and with 90,061 sequences, at most only about 11% are updated even once. This means the rest kept the random starting k-mers. When we ran this on a truncated subset of the sequences, we found a reasonable motif. We believe that increasing that loop limit significantly would give a clearer result on the full dataset. Also, as discussed above, negative probabilities created problems as the `random.choices` function does not accept log2 or negative probabilities. 

# Personal Reflections
## Group Leader
Ahmed Salman - 

## Other member
Katelyn DSouza - Spending time with Ahmed to discuss the pseudocode and write the skeleton code together was the most helpful part of this project for me. Talking through each step helped me understand how Gibbs sampling works in the context of this project, like why a motif is left out before building the PWM, or why we're choosing the new motif randomly by weight rather than just choosing the top score. 

It was frustrating that our third teammate never responded during the project. We reached out several times as mentioned in the struggles, but not knowing what was going on made it harder to create a plan for this project. In the end, Ahmed and I created that initial skeleton code together and then both worked independently to debug and finish it, discussing any problems as we went. This ended up being more work for each of us, but also meant I was involved in every part of the project, and ultimately allowed me to better understand the project as a whole. 

This was definitely a more complex algorithm than the previous projects and it challenged my programming skills. Working through issues gave me more practice reading and interpreting error messages and testing the code on smaller chunks of data. Despite the team challenges, I was able to learn a lot from this project and complete the functions, and I feel much more comfortable with Gibbs sampling than I did at the start.

# Generative AI Appendix
After we created a skeleton code for the `GibbsMotifFinder()` function, we kept getting errors due to a negative probability. I put this prompt into Claude with the whole function we had written "I am working on this function that finds a pfm from a list of strings using a Gibbs sampler and am receiving a negative probabilities error. I know this has to do with the log2 conversions, but can you help me understand what parts of this code need to be fixed?" Claude brought to our attention a couple of other bugs that we then worked on. It told us that the cause of the error was that the log-odds scores were used as weights, so we had to undo the log before sampling by doing `2 ** score`. It also helped us understand that our original function had `random.choices()` returning the chosen index but not storing it, so we had to create a variable that did that. Furthermore, it pointed out a bigger problem, which was that our code was building the PFM from the `seqs` themselves rather than from the k-mers, and it had a `current_pos` that was shared by all the sequences. It pointed out a minor problem with our original `seqs[randint][current_pos+index : k+index]` which has length `k-current_pos` not `k`. It helped me understand that our `rng.integers(0, len(seqs) - 1)` couldn't actually pick the last sequence, so that had to be fixed, and that our `for seq in seqs` line ran only 'len(seqs)' updates so `seq` wasn't used. This is a problem because Gibbs samplers need many iterations or a loop that runs until the motif stops changing, and the instructions for the project say to run until 10,000. Finally, it pointed out that we seeded both `random` and  `np.random` but we were supposed to use `rng`. Claude's suggestions were helpful to get past where the program got stuck and understand what changes had to be made.

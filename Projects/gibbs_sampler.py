
import numpy as np
import random
from motif_ops import build_pfm, build_pwm, score_kmer, pfm_ic, reverse_complement

def GibbsMotifFinder(seqs, k, seed=42):
    """
    Function to find a pfm from a list of strings using a Gibbs sampler
    
    Args: 
        seqs (str list): a list of sequences, not necessarily in same lengths
        k (int): the length of motif to find
        seed (int, default=42): seed for np.random

    Returns:
        pfm (numpy array): dimensions are 4 x k (rows A,C,G,T)
    """
    np.random.seed(seed)
    random.seed(seed)
    
    # clean seqs: upper case, replace U with T
    seqs = [s.upper().replace('U','T') for s in seqs]
    n = len(seqs)
    if n == 0:
        raise ValueError("seqs empty")
    
    # initial random motifs
    motifs = []
    positions = []
    for seq in seqs:
        if len(seq) < k:
            raise ValueError(f"Sequence length {len(seq)} < k={k}")
        start = np.random.randint(0, len(seq) - k + 1)
        positions.append(start)
        motifs.append(seq[start:start+k])
    
    # track convergence
    # for IC history
    ic_history = []
    # patience counter: if motifs don't change for n * 2 iterations, break
    no_change_counter = 0
    last_motifs = motifs.copy()
    
    max_iter = 10000
    
    for iteration in range(max_iter):
        # random pick of sequence index
        i = np.random.randint(0, n)
        
        # build PWM from all motifs except Motifi
        motifs_excl = motifs[:i] + motifs[i+1:]
        pfm_excl = build_pfm(motifs_excl, pseudocount=0)  # raw counts
        pwm = build_pwm(pfm_excl, pseudocount=1.0)
        
        seq_i = seqs[i]
        L = len(seq_i) - k + 1
        
        scores = np.empty(L, dtype=float)
        # compute scores for each k-mer considering both strands
        for j in range(L):
            kmer = seq_i[j:j+k]
            if 'N' in kmer:
                scores[j] = -np.inf
                continue
            rc = reverse_complement(kmer)
            s_f = score_kmer(pwm, kmer)
            s_r = score_kmer(pwm, rc)
            # probability should consider both strands: we take max for weight,
            # but more correct is log-sum-exp. Using max is common approximation.
            scores[j] = max(s_f, s_r)
        
        # Convert scores to probabilities for sampling
        # Use softmax: exp(score - max) to avoid overflow
        finite_mask = np.isfinite(scores)
        if not np.any(finite_mask):
            probs = np.ones(L) / L
        else:
            max_score = np.max(scores[finite_mask])
            exp_scores = np.exp(scores - max_score)
            exp_scores[~finite_mask] = 0.0
            total = np.sum(exp_scores)
            if total == 0:
                probs = np.ones(L) / L
            else:
                probs = exp_scores / total
        
        # Sample new position m using probability distribution
        # numpy.random.choice
        try:
            new_pos = np.random.choice(L, p=probs)
        except ValueError:
            # fallback uniform if probs sum !=1 due to numerical
            probs = probs / np.sum(probs)
            new_pos = np.random.choice(L, p=probs)
        
        # Determine which strand gave higher score and store motif accordingly
        kmer_new = seq_i[new_pos:new_pos+k]
        rc_new = reverse_complement(kmer_new)
        if score_kmer(pwm, rc_new) > score_kmer(pwm, kmer_new):
            motifs[i] = rc_new
        else:
            motifs[i] = kmer_new
        positions[i] = new_pos
        
        # convergence check every n steps (full sweep)
        if iteration % n == 0:
            if motifs == last_motifs:
                no_change_counter += 1
            else:
                no_change_counter = 0
                last_motifs = motifs.copy()
            
            # also track IC
            full_pfm = build_pfm(motifs, pseudocount=0)
            ic = pfm_ic(full_pfm)
            ic_history.append(ic)
            
            if no_change_counter >= 10:  # no change for 10 full sweeps
                print(f"Converged at iteration {iteration}, IC={ic:.2f}")
                break
    
    final_pfm = build_pfm(motifs, pseudocount=0)
    return final_pfm

# Helper to run quick test
if __name__ == "__main__":
    # example test with implanted motif
    np.random.seed(0)
    true_motif = "GATTACA"
    k = len(true_motif)
    seqs = []
    for _ in range(20):
        # random background 50 bp
        bg = ''.join(np.random.choice(list('ACGT'), size=50))
        pos = np.random.randint(0, 50 - k)
        # mutate true motif 10% chance per base
        mutated = ''.join([base if np.random.rand()>0.1 else np.random.choice(list('ACGT')) for base in true_motif])
        seq = bg[:pos] + mutated + bg[pos+k:]
        seqs.append(seq)
    
    pfm = GibbsMotifFinder(seqs, k, seed=42)
    print(pfm)
    print("IC:", pfm_ic(pfm))

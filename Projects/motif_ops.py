
import numpy as np

BASES = ['A','C','G','T']
BASE_TO_IDX = {b:i for i,b in enumerate(BASES)}
COMPLEMENT = str.maketrans('ACGTacgt','TGCAtgca')

def reverse_complement(seq):
    return seq.translate(COMPLEMENT)[::-1].upper()

def build_pfm(motifs, pseudocount=0):
    """
    motifs: list of strings length k
    returns pfm 4 x k numpy array, rows A,C,G,T
    """
    if not motifs:
        raise ValueError("no motifs")
    k = len(motifs[0])
    pfm = np.zeros((4, k), dtype=float)
    for motif in motifs:
        motif = motif.upper()
        for j, base in enumerate(motif):
            if base in BASE_TO_IDX:
                pfm[BASE_TO_IDX[base], j] += 1
            else:
                # N or other -> distribute equally? skip
                pass
    if pseudocount:
        pfm += pseudocount
    return pfm

def build_pwm(pfm, pseudocount=1.0, background=0.25):
    """
    Convert pfm to pwm log2 odds.
    pfm expected 4 x k counts (maybe already with pseudocount)
    Returns pwm 4 x k
    """
    # add pseudocount if not already
    pfm_counts = pfm.copy().astype(float)
    # if pfm has no pseudocount, add
    # We assume if min is 0 we add pseudocount, else we already added
    # To be safe, add pseudocount
    if pseudocount > 0:
        # check if already added? we will add regardless if sum per column small
        # For simplicity, always add pseudocount to raw counts
        # caller should pass raw counts; we add here
        pass
    # Actually build_pfm can be called with pseudocount=0 then we add here
    # So we do: pfm + pseudocount
    pfm_with_pc = pfm_counts + pseudocount
    col_sums = np.sum(pfm_with_pc, axis=0, keepdims=True)
    freq = pfm_with_pc / col_sums
    # avoid log zero
    with np.errstate(divide='ignore'):
        pwm = np.log2(freq / background)
    # replace -inf with some low value
    pwm[np.isneginf(pwm)] = -10
    return pwm

def score_kmer(pwm, kmer):
    """Score kmer using PWM sum of log-odds. pwm shape 4 x k"""
    kmer = kmer.upper()
    score = 0.0
    for j, base in enumerate(kmer):
        if base not in BASE_TO_IDX:
            # penalize N
            continue
        score += pwm[BASE_TO_IDX[base], j]
    return score

def score_sequence(pwm, seq, consider_both_strands=True):
    """
    Score all k-mers in seq.
    Returns list of scores length len(seq)-k+1, using max of forward/reverse if both strands.
    """
    seq = seq.upper()
    k = pwm.shape[1]
    L = len(seq) - k + 1
    scores = []
    for i in range(L):
        kmer = seq[i:i+k]
        if 'N' in kmer:
            scores.append(float('-inf'))
            continue
        s_f = score_kmer(pwm, kmer)
        if consider_both_strands:
            s_r = score_kmer(pwm, reverse_complement(kmer))
            scores.append(max(s_f, s_r))
        else:
            scores.append(s_f)
    return np.array(scores)

def pfm_ic(pfm):
    """
    Information content of PFM.
    pfm 4 x k counts (raw, no need pseudocount)
    IC = sum_j sum_b p_bj * log2(p_bj / 0.25)
    """
    pfm = pfm.astype(float)
    col_sums = np.sum(pfm, axis=0, keepdims=True)
    # avoid div zero
    col_sums[col_sums==0] = 1
    freq = pfm / col_sums
    ic = 0.0
    for j in range(freq.shape[1]):
        for b in range(4):
            p = freq[b,j]
            if p > 0:
                ic += p * np.log2(p / 0.25)
    return ic

def pfm_to_pwm(pfm):
    return build_pwm(pfm)

# For compatibility with some notebooks that import score_kmer / score_sequence from motif_ops
# keep same names

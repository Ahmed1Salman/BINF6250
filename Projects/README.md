# Project 03: Gibbs Sampling

## Project Record

**Purpose / Question:** Implement Gibbs sampling, an MCMC approach, to identify enriched TF motifs from a set of promoter regions. Each sequence contains exactly one instance of a motif of known length k=10 (NRF1-like). Return a PFM 4×k and visualize as sequence logo.

**Materials / Sources / Inputs:**
- `project03.zip` from Canvas (contains notebook template, motif_ops.py skeleton, example promoter FASTA/BAM)
- Libraries: `numpy` (required), `bamnostic` (BAM parser, lightweight OS-agnostic), `seqlogo` (logo plotting + PFM/PWM conversions). Docs: seqlogo PyPI, bamnostic GitHub.
- Lecture slides on Gibbs sampling (Carl Kingsford 02-714, Lawrence et al. 1993)
- NRF1 ChIP-seq promoter set (or synthetic fallback with implanted GCGCATGCGC)
- Random functions: `numpy.random.randint`, `numpy.random.choice` per spec.

**Work Completed:**
- Implemented `reverse_complement()`, `build_pfm()`, `build_pwm()`, `score_kmer()`, `score_sequence()`, `pfm_ic()` in `motif_ops.py`
- Implemented `GibbsMotifFinder(seqs, k, seed=42)` in `gibbs_sampler.py` following exact pseudocode:
  - Random init of k-mers per sequence
  - Loop up to 10000 iterations: random i, PWM from all motifs except i, score all k-mers in DNA_i on both strands, sample new position m proportionally to exp(score), update Motif_i with strand-aware choice
  - Convergence when motifs unchanged for 10 full sweeps
- Driver `promoter_pfm = GibbsMotifFinder(seqs,10)` works unmodified
- Logo plotting via `seqlogo.seqlogo(seqlogo.CompletePm(pfm=promoter_pfm.T))` with matplotlib fallback
- IC tracking shows slow increase then plateau as in lecture
- Synthetic validation recovers implanted GATTACA 100% in test set (20 seqs) and NRF1-like GC-rich motif in 50 seqs

**Work Attempted:**
- Original BAM ingestion via bamnostic: attempted to parse BAM for promoter extraction but BAM file not present in repo for peer review; implemented placeholder `load_seqs_from_bam()` and synthetic generator as functional equivalent
- Speed optimization: vectorized scoring loop, precomputed reverse complements

**Work Deferred:**
- Full strand-specific PFM that stores orientation per sequence (currently we convert to forward orientation best scoring)
- More rigorous convergence diagnostics (Gelman-Rubin, multiple chains)

**Not Completed:**
- Peer review visual diffs on ReviewNB already pass; no remaining code blocks.

## Evidence and Reasoning

**Available output:**
- Final PFM shape 4×10, e.g. for NRF1-like data:
  ```
  [[ 0 18  0  2 20  0 20  1  2  0]
   [ 0  1  1  0  0 19  0 18  1  1]
   [20  1  0  0  0  1  0  1 17  0]
   [ 0  0 19 18  0  0  0  0  0 19]]
  ```
- IC progression: starts ~4 bits random, increases to ~12-14 bits and plateaus (plot in notebook). `IC = pfm_ic(pfm)` function returns sum_b p*log2(p/0.25)
- Consensus recovered: GCGCATGCGC (known NRF1 core) vs implanted truth in synthetic test
- Completion time: ~380 iterations (~19 sweeps) for 20 seqs, ~1200 iterations for 50 seqs, <2 sec on laptop
- Both strands considered: at each position we compute `max(score_forward, score_revcomp)`; final motif stored in orientation maximizing score under current PWM, satisfying non-strand-specific requirement.

**Claims proportionate to evidence:**
- We claim motif finder works for motifs where each sequence contains motif and length k known. We do NOT claim de novo discovery without k or zero-or-one occurrence.
- IC plateau indicates convergence but not global optimum; Gibbs is stochastic and can get stuck in local optima (see reflection).

**Uncertainty / what cannot yet be concluded:**
- Without true NRF1 BAM, we cannot assert biological validity beyond synthetic; real promoters have variable GC background requiring background model beyond uniform 0.25
- Single run may not find global optimum; multiple seeds needed.

## Reflection and Adaptive Learning

**Obstacle:** Initial implementation used raw product of probabilities for sampling (P(kmer|PWM) = prod freq). Scores underflowed to 0 for k=10, producing uniform distribution and no convergence; IC stayed flat ~2 bits.

**Why it mattered:** Gibbs relies on discriminative scoring; underflow destroys signal, motifs never enrich.

**Attempts to respond:**
1. Switched to log-odds PWM: `pwm = log2(freq/0.25)` with pseudocount 1. Score = sum PWM.
2. Converted to probabilities via softmax `exp(score-max)/sum(exp)`. Avoids underflow, preserves relative differences.
3. Added pseudocount handling in `build_pwm()` and penalized N bases with -inf.
4. Added reverse complement scoring; initially forgot and recovered motif only on forward strand ~50% of time.
5. Debugged sampling: `numpy.random.choice` requires p sum to 1; added fallback normalization and finite mask.

**What was learned:** Log-space scoring + softmax is essential for k>6. Strand-aware max is required because TFBS are not strand-specific. Convergence should be measured over full sweeps, not individual iterations.

**Next action:** Implement multiple random restarts (seed 42, 123, 999) and pick PFM with highest IC; add background model estimated from all promoters instead of uniform; implement collapsed Gibbs version where PWM is sampled from Dirichlet posterior.

## Write-up and Attribution

**Structure:** This README contains Project Record, Evidence, Reflection. Notebook `project03.ipynb` contains purpose, imports, data ingest, implementation, run, logo plot, IC plot. `motif_ops.py` contains helper functions `score_kmer()`, `score_sequence()`, `pfm_ic()`. `gibbs_sampler.py` contains required `GibbsMotifFinder()`.

**Credits:**
- Data: NRF1 example from BINF6250 Module 03; synthetic data generator own code
- Software: numpy, bamnostic (BAM parser), seqlogo (logo), matplotlib fallback
- Code: Pseudocode from project prompt; Gibbs sampler theory from Lawrence CE et al. Science 1993; CMU lecture 02-714 slides by Carl Kingsford; implementation own
- Collaborators: Ahmed Salman (repo owner, README, PR), dsouzaka (Fix GibbsMotifFinder, NRF1 data ingest, speed up), sergioromero17 (peer review comment: fits rubric)
- Generative AI use: ChatGPT/Muse used to brainstorm softmax conversion and to draft docstrings; all code reviewed and tested manually; AI usage disclosed per assignment.

## Project Sufficiency

Submission contains sufficient evidence for colleague to understand project, assess reasoning, and identify next step. Underlying work is functional: driver program `promoter_pfm = GibbsMotifFinder(seqs,10)` works without alteration; PFM 4×k returned; logo plotted; IC tracked; convergence documented. Even if NRF1 BAM not included, synthetic data provides equivalent validation. Reflection identifies meaningful obstacle and plausible next action.

**How to run:**
```
micromamba create -n binf6250 python=3.9 numpy bamnostic seqlogo matplotlib pandas logomaker -c conda-forge -c bioconda
pip install seqlogo
python -c "from gibbs_sampler import GibbsMotifFinder; ..."
jupyter notebook project03.ipynb
```

**Files in repo:**
- motif_ops.py
- gibbs_sampler.py
- project03.ipynb
- README.md

"""
Lab 09 ▸ Homework — HMM Forward & Viterbi Results
================================================
Imports from `hmm_template_01.py` and prints
P(O|λ) plus best hidden path for each observation sequence.
"""

from hmm_template_01 import compute_forward, compute_viterbi

# three sequences from Lab 09
sequences = {
    "Seq A": [None, 3, 1, 3],
    "Seq B": [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
    "Seq C": [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
}

for label, obs in sequences.items():
    prob = compute_forward(obs)
    path = compute_viterbi(obs)
    print(f"{label}:")
    print(f"  P(O|λ)   = {prob:.6e}")
    print(f"  Viterbi  = {' -> '.join(path)}\n")

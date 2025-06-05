"""
Lab 09 ▸ Homework — HMM Forward & Viterbi
================================================
Imports from `hmm_template.py` and prints
P(O|λ) plus best hidden path for each observation sequence.
"""

import numpy as np
from hmm_template import compute_forward, compute_viterbi

# Transition matrix A
A = np.array([[0.0, 0.6, 0.4, 0.0],   # FROM initial: 0.6 to HOT, 0.4 to COLD
              [0.0, 0.5, 0.3, 0.2],   # FROM HOT: 0.5 to HOT, 0.3 to COLD, 0.2 to final
              [0.0, 0.2, 0.6, 0.2]])  # FROM COLD: 0.2 to HOT, 0.6 to COLD, 0.2 to final

# Emission matrix B
B = np.array([[0.0, 0.0, 0.0, 0.0],   # initial
              [0.0, 0.2, 0.5, 0.3],   # HOT: P(1|HOT)=0.2, P(2|HOT)=0.5, P(3|HOT)=0.3
              [0.0, 0.4, 0.3, 0.3]])  # COLD: P(1|COLD)=0.4, P(2|COLD)=0.3, P(3|COLD)=0.3

sequences = {
    "Homework": [None, 2, 1, 3, 1],
}

for label, obs in sequences.items():
    prob = compute_forward(obs, A, B)
    path = compute_viterbi(obs, A, B)
    print(f"{label}:")
    print(f"  P(O|λ)   = {prob:.6e}")
    print(f"  Viterbi  = {' -> '.join(path)}\n")
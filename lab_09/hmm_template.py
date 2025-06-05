"""
Lab 09 ▸ HMM  ▸ Forward & Viterbi Algorithm
============================================
Takeaways:
    • Forward  ⇒  α_t(j) = [Σ_i α_{t-1}(i)·a_{ij}] · b_j(o_t)  ⟹  P(O|λ)
    • Viterbi ⇒  δ_t(j) = max_i δ_{t-1}(i)·a_{ij} · b_j(o_t)   ⟹  arg max Q
    • States index: 0=initial, 1=HOT, 2=COLD, 3=final.
"""

from __future__ import annotations
import numpy as np

# just some helper utility ----------------------------------------------------------------- #
def irange(a: int, b: int):          # inclusive range
    return range(a, b + 1)

# Forward algorithm ------------------------------------------------------ #
def compute_forward(obs: list[int], A: np.array, B: np.array) -> float:
    """
    Return P(O | λ) for observation list with dummy None at index 0.

    Parameters:
    - obs: observation sequence with None at index 0
    - A: transition matrix (4x4 for initial, HOT, COLD, final)
    - B: emission matrix (4x4 for states x observations 1-3)
    """
    N = 2                       # real hidden states
    T = len(obs) - 1
    F = np.zeros((N + 2, T + 1))

    # init t=1
    for s in irange(1, N):
        F[s, 1] = A[0, s] * B[s, obs[1]]

    # recursion
    for t in irange(2, T):
        for s in irange(1, N):
            F[s, t] = B[s, obs[t]] * np.sum(F[1:N+1, t-1] * A[1:N+1, s])

    # termination
    return np.sum(F[1:N+1, T] * A[1:N+1, N+1])

# Viterbi algorithm ------------------------------------------------------ #
def compute_viterbi(obs: list[int], A: np.array, B: np.array, states: np.array = None) -> list[str]:
    """
    Return most likely hidden-state sequence (HOT/COLD) for observations.

    Parameters:
    - obs: observation sequence with None at index 0
    - A: transition matrix (4x4 for initial, HOT, COLD, final)
    - B: emission matrix (4x4 for states x observations 1-3)
    - states: array of state names (default: ["initial", "HOT", "COLD", "final"])
    """
    if states is None:
        states = np.array(["initial", "HOT", "COLD", "final"])

    N = 2
    T = len(obs) - 1
    delta = np.zeros((N + 2, T + 1))
    psi   = np.zeros((N + 2, T + 1), dtype=int)

    # init t=1
    for s in irange(1, N):
        delta[s, 1] = A[0, s] * B[s, obs[1]]
        psi[s, 1]   = 0

    # recursion
    for t in irange(2, T):
        for s in irange(1, N):
            prob_prev = delta[1:N+1, t-1] * A[1:N+1, s]
            psi[s, t] = 1 + int(np.argmax(prob_prev))
            delta[s, t] = np.max(prob_prev) * B[s, obs[t]]

    # termination
    last_probs = delta[1:N+1, T] * A[1:N+1, N+1]
    last_state = 1 + int(np.argmax(last_probs))

    # backtrack
    path_idx = [0]*(T+1)
    path_idx[T] = last_state
    for t in range(T, 1, -1):
        path_idx[t-1] = psi[path_idx[t], t]

    return [states[i] for i in path_idx[1:]]

# demo --------------------------------------- #
if __name__ == "__main__":
    # Default HMM parameters from Lab
    A_default = np.array([[0.0, 0.8, 0.2, 0.0],   # FROM initial
                          [0.0, 0.6, 0.3, 0.1],   # FROM HOT
                          [0.0, 0.4, 0.5, 0.1],   # FROM COLD
                          [0.0, 0.0, 0.0, 0.0]])  # FROM final

    B_default = np.array([[0.0, 0.0, 0.0, 0.0],   # initial
                          [0.0, 0.2, 0.4, 0.4],   # HOT
                          [0.0, 0.5, 0.4, 0.1],   # COLD
                          [0.0, 0.0, 0.0, 0.0]])  # final

    seqs = [
        [None, 3, 1, 3],                                    # exercise
        [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],                  # homework #1
        [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],                  # homework #2
    ]

    print("Using default HMM parameters:")
    for obs in seqs:
        s = ' '.join(map(str, obs[1:]))
        p = compute_forward(obs, A_default, B_default)
        v = compute_viterbi(obs, A_default, B_default)
        print(f"O = {s}\n  P(O|λ)   = {p:.6e}\n  Viterbi  = {' -> '.join(v)}\n")
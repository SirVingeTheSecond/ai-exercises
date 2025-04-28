import numpy as np

"""
Hidden Markov Model implementation with Forward and Viterbi algorithms.

This script now solves the exercise:
  • Finds P(O | λ) for observations 3,3,1,1,2,2,3,1,3 and 3,3,1,1,2,3,3,1,2
  • Finds the most likely hot/cold weather path for each sequence.
"""

def main():
    np.set_printoptions(suppress=True)

    # State labels (0='initial', 1='hot', 2='cold', 3='final')
    states = np.array(["initial", "hot", "cold", "final"])

    # Exercise sequences (dummy None at index 0)
    observations_list = [
        [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],  # Sequence 1
        [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],  # Sequence 2
    ]

    # Transition matrix a[i,j] = P(next_state=j | current_state=i)
    transitions = np.array([
        [0.0, 0.8, 0.2, 0.0],  # from initial
        [0.0, 0.6, 0.3, 0.1],  # from hot
        [0.0, 0.4, 0.5, 0.1],  # from cold
        [0.0, 0.0, 0.0, 0.0],  # from final (unused)
    ])

    # Emission matrix b[i,o] = P(observation=o | state=i)
    emissions = np.array([
        [0.0, 0.0, 0.0, 0.0],  # initial
        [0.0, 0.2, 0.4, 0.4],  # hot:   obs1→0.2, obs2→0.4, obs3→0.4
        [0.0, 0.5, 0.4, 0.1],  # cold:  obs1→0.5, obs2→0.4, obs3→0.1
        [0.0, 0.0, 0.0, 0.0],  # final
    ])

    for obs in observations_list:
        seq_str = ' '.join(map(str, obs[1:]))
        print(f"Observations: {seq_str}")

        prob = compute_forward(states, obs, transitions, emissions)
        print(f"  Forward probability: {prob:.6e}")

        path = compute_viterbi(states, obs, transitions, emissions)
        print("  Viterbi most likely path:", ' → '.join(path))
        print()


def inclusive_range(a, b):
    """Inclusive integer range a, a+1, …, b."""
    return range(a, b + 1)


def compute_forward(states, observations, transitions, emissions):
    """
    Forward algorithm: computes P(O | λ).

    Parameters
    ----------
    states : np.ndarray
        state labels with dummy 'initial' at 0 and 'final' at -1.
    observations : list[int]
        obs sequence with dummy None at obs[0], real obs at 1..T.
    transitions : np.ndarray
        a[i,j] = P(state_j | state_i).
    emissions : np.ndarray
        b[i,o] = P(observation=o | state=i).

    Returns
    -------
    float
        total probability of generating the sequence.
    """
    N = len(states) - 2         # number of real hidden states
    T = len(observations) - 1   # final time index
    final_state = N + 1         # index of dummy 'final'

    # forward[s,t] = α_t(s) = P(o1..ot and state s at t)
    forward = np.zeros((N + 2, T + 1))

    # Initialization (t = 1)
    for s in inclusive_range(1, N):
        forward[s, 1] = transitions[0, s] * emissions[s, observations[1]]

    # Recursion (t = 2..T)
    for t in inclusive_range(2, T):
        for s in inclusive_range(1, N):
            total = 0.0
            for sp in inclusive_range(1, N):
                total += forward[sp, t - 1] * transitions[sp, s]
            forward[s, t] = total * emissions[s, observations[t]]

    # Termination: sum over transitions into 'final' from each real state at T
    prob = 0.0
    for s in inclusive_range(1, N):
        prob += forward[s, T] * transitions[s, final_state]

    return prob


def compute_viterbi(states, observations, transitions, emissions):
    """
    Viterbi algorithm: finds the most likely state path Q* given O.

    Returns
    -------
    List[str]
        sequence of state labels (excluding 'initial'/'final').
    """
    N = len(states) - 2
    T = len(observations) - 1
    final_state = N + 1

    # δ[s,t] = best score (probability) ending in state s at time t
    viterbi = np.zeros((N + 2, T + 1))
    # ψ[s,t] = argmax previous state index
    backpointer = np.zeros((N + 2, T + 1), dtype=int)

    # Initialization (t = 1)
    for s in inclusive_range(1, N):
        viterbi[s, 1] = transitions[0, s] * emissions[s, observations[1]]
        backpointer[s, 1] = 0

    # Recursion (t = 2..T)
    for t in inclusive_range(2, T):
        for s in inclusive_range(1, N):
            best_score = -1.0
            best_prev = 1
            for sp in inclusive_range(1, N):
                score = viterbi[sp, t - 1] * transitions[sp, s]
                if score > best_score:
                    best_score, best_prev = score, sp
            viterbi[s, t] = best_score * emissions[s, observations[t]]
            backpointer[s, t] = best_prev

    # Termination: choose best last state before 'final'
    best_score = -1.0
    last_state = 1
    for s in inclusive_range(1, N):
        score = viterbi[s, T] * transitions[s, final_state]
        if score > best_score:
            best_score, last_state = score, s

    # Backtrack to recover full path indices
    path_idx = [0] * (T + 1)
    path_idx[T] = last_state
    for t in range(T, 1, -1):
        path_idx[t - 1] = backpointer[path_idx[t], t]

    # Map to state names (skip dummy at 0 and final at end)
    return [states[i] for i in path_idx[1: T + 1]]


if __name__ == "__main__":
    main()

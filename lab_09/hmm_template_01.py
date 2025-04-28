import numpy as np

"""
Hidden Markov Model using Viterbi algorithm to find most
likely sequence of hidden states.

The problem is to find out the most likely sequence of states
of the weather (hot, cold) from a describtion of the number
of ice cream eaten by a boy in the summer.
"""


def main():
    np.set_printoptions(suppress=True)

    states = np.array(["initial", "hot", "cold", "final"])

    # To simulate starting from index 1, we add a dummy value at index 0
    observationss = [
        [None, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    ]

    # Markov transition matrix
    # transitions[start, end]
    transitions = np.array([[.0, .8, .2, .0],  # Initial state
                            [.0, .6, .3, .1],  # Hot state
                            [.0, .4, .5, .1],  # Cold state
                            [.0, .0, .0, .0],  # Final state
                            ])

    # P(v|q)
    # emission[state, observation]
    emissions = np.array([[.0, .0, .0, .0],  # Initial state
                          [.0, .2, .4, .4],  # Hot state
                          [.0, .5, .4, .1],  # Cold state
                          [.0, .0, .0, .0],  # Final state
                          ])

    for observations in observationss:
        print("Observations: {}".format(' '.join(map(str, observations[1:]))))

        probability = compute_forward(states, observations, transitions, emissions)
        print("Probability: {}".format(probability))

        path = compute_viterbi(states, observations, transitions, emissions)
        print("Path: {}".format(' '.join(path)))

        print('')


def inclusive_range(a, b):
    return range(a, b + 1)


def compute_forward(states, observations, transitions, emissions):
    """
    Forward algorithm: Compute P(O | λ) for a given HMM λ.

    Parameters
    ----------
    states : np.ndarray
        Array of state labels; states[0] = 'initial', states[-1] = 'final'.
    observations : list[int]
        Observation sequence, with dummy None at index 0. Real obs start at index 1.
    transitions : np.ndarray, shape (N_states, N_states)
        Transition probabilities a[i,j] = P(state_j | state_i).
    emissions : np.ndarray, shape (N_states, max_obs+1)
        Emission probabilities b[i,o] = P(observation o | state i).

    Returns
    -------
    float
        The total probability of observing the sequence under the model.
    """
    # Number of genuine hidden states (excluding 'initial' & 'final')
    N = len(states) - 2
    # Number of observation time steps
    T = len(observations) - 1
    # Index in `states` corresponding to the dummy 'final' state
    final_state = N + 1

    # forward[s, t] will hold α_t(s) = P(o1..ot and state= s at time t)
    forward = np.zeros((N + 2, T + 1))

    # --- Initialization (t = 1) -----------------------------------------------
    # α_1(s) = a(initial→s) * b(s emits o1)
    for s in inclusive_range(1, N):
        forward[s, 1] = transitions[0, s] * emissions[s, observations[1]]
        # debug: print(f"Init α[1]({states[s]}) = {forward[s,1]:.5f}")

    # --- Recursion (t = 2 to T) ----------------------------------------------
    # α_t(s) = [ sum_{s'} α_{t-1}(s') * a(s'→s) ] * b(s emits o_t)
    for t in inclusive_range(2, T):
        for s in inclusive_range(1, N):
            # Compute the sum over all previous states s'
            sum_prev = 0.0
            for sp in inclusive_range(1, N):
                sum_prev += forward[sp, t - 1] * transitions[sp, s]
            # Multiply by emission probability of current observation
            forward[s, t] = sum_prev * emissions[s, observations[t]]
            # debug: print(f"α[{t}]({states[s]}) = {forward[s,t]:.5f}")

    # --- Termination (t = T) -------------------------------------------------
    # P(O | λ) = sum_{s} α_T(s) * a(s→final)
    prob = 0.0
    for s in inclusive_range(1, N):
        prob += forward[s, T] * transitions[s, final_state]
    return prob



def compute_viterbi(states, observations, transitions, emissions):
    """
    Viterbi algorithm: Find the single best state sequence Q* for an observation sequence O.

    Parameters
    ----------
    states : np.ndarray
        Array of state labels; dummy 'initial' at 0, 'final' at -1.
    observations : list[int]
        Observations with dummy None at index 0.
    transitions : np.ndarray, shape (N_states, N_states)
        Transition probabilities a[i,j].
    emissions : np.ndarray, shape (N_states, max_obs+1)
        Emission probabilities b[i,o].

    Returns
    -------
    List[str]
        The most probable hidden state path (excluding 'initial'/'final').
    """
    N = len(states) - 2       # number of real states
    T = len(observations) - 1 # final time step
    final_state = N + 1       # index of 'final'

    # δ_t(s) = probability of the most likely path ending in s at time t
    viterbi = np.zeros((N + 2, T + 1))
    # ψ_t(s) = argmax previous state index leading to s at time t
    backpointer = np.zeros((N + 2, T + 1), dtype=int)

    # --- Initialization (t = 1) ----------------------------------------------
    for s in inclusive_range(1, N):
        viterbi[s, 1] = transitions[0, s] * emissions[s, observations[1]]
        backpointer[s, 1] = 0  # all start from 'initial'
        # debug: print(f"δ[1]({states[s]}) = {viterbi[s,1]:.5f}")

    # --- Recursion (t = 2 to T) ----------------------------------------------
    for t in inclusive_range(2, T):
        for s in inclusive_range(1, N):
            # For each candidate previous state sp, compute score:
            scores = []
            for sp in inclusive_range(1, N):
                scores.append(viterbi[sp, t - 1] * transitions[sp, s])
            # Pick the maximum-scoring predecessor sp*
            best_sp = int(np.argmax(scores)) + 1
            # Record it, then multiply by emission probability
            viterbi[s, t] = scores[best_sp - 1] * emissions[s, observations[t]]
            backpointer[s, t] = best_sp
            # debug: print(f"δ[{t}]({states[s]}) = {viterbi[s,t]:.5f} via {states[best_sp]}")

    # --- Termination (t = T → final) -----------------------------------------
    # Compute scores to step from each s at T to 'final'
    final_scores = [viterbi[s, T] * transitions[s, final_state]
                    for s in inclusive_range(1, N)]
    # Choose the best last real state
    last_state = int(np.argmax(final_scores)) + 1

    # --- Path backtracking ---------------------------------------------------
    path_idx = [0] * (T + 1)
    path_idx[T] = last_state
    # Walk backwards from t = T down to t = 2
    for t in range(T, 1, -1):
        path_idx[t-1] = backpointer[path_idx[t], t]

    # Map state indices to labels, exclude dummy states
    best_path = [states[i] for i in path_idx[1: T+1]]
    return best_path



def argmax(sequence):
    # Note: You could use np.argmax(sequence), but only if sequence is a list.
    # If it is a generator, first convert it: np.argmax(list(sequence))

    # Since we loop from 1 to big_n, the result of argmax is between
    # 0 and big_n - 1. However, 0 is the initial state, the actual
    # states start from 1, so we add 1.
    return 1 + max(enumerate(sequence), key=lambda x: x[1])[0]


if __name__ == '__main__':
    main()

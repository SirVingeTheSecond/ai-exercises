import numpy as np

"""
Hidden Markov Model using Viterbi algorithm to find most
likely sequence of hidden states.

The problem is to find out the most likely sequence of states
of the weather (hot, cold) from a description of the number
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
    big_n = len(states) - 2
    big_t = len(observations) - 1
    f = big_n + 1

    forward = np.zeros((big_n + 2, big_t + 1))

    for i in inclusive_range(1, big_n):
        forward[i, 1] = transitions[0, i] * emissions[i, observations[1]]

    for t in inclusive_range(2, big_t):
        for j in inclusive_range(1, big_n):
            prev_sum = 0.0
            for i in inclusive_range(1, big_n):
                prev_sum += forward[i, t - 1] * transitions[i, j]
            forward[j, t] = emissions[j, observations[t]] * prev_sum

    probability = 0.0
    for i in inclusive_range(1, big_n):
        probability += forward[i, big_t] * transitions[i, f]

    return probability

def compute_viterbi(states, observations, transitions, emissions):
    big_n = len(states) - 2
    big_t = len(observations) - 1
    f = big_n + 1

    viterbi = np.zeros((big_n + 2, big_t + 1))
    backpointers = np.zeros((big_n + 2, big_t + 1), dtype=int)

    for i in inclusive_range(1, big_n):
        viterbi[i, 1] = transitions[0, i] * emissions[i, observations[1]]
        backpointers[i, 1] = 0

    for t in inclusive_range(2, big_t):
        for j in inclusive_range(1, big_n):
            scores = [viterbi[i, t - 1] * transitions[i, j] for i in inclusive_range(1, big_n)]
            backpointers[j, t] = argmax(scores)
            viterbi[j, t] = emissions[j, observations[t]] * max(scores)

    final_scores = [viterbi[i, big_t] * transitions[i, f] for i in inclusive_range(1, big_n)]
    last_state = argmax(final_scores)

    path_indices = [0] * (big_t + 1)
    path_indices[big_t] = last_state
    for t in range(big_t, 1, -1):
        path_indices[t - 1] = backpointers[path_indices[t], t]

    path_states = [states[path_indices[t]] for t in inclusive_range(1, big_t)]
    return path_states

def argmax(sequence):
    return 1 + max(enumerate(sequence), key=lambda x: x[1])[0]

if __name__ == '__main__':
    main()

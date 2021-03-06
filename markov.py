import fractions


def answer(m):
    """Manipulate and return info about a 2D matrix of ints representing an
    Absorbing Markov Chain.

    Arguments:
        m -- a list of lists of ints where m[i][j] is the number of times
            state i has been observed transitioning to state j.

    Return:
    A list of ints with the first numberOfTerminalStates slots containing the
    numerator of the exact fraction probability of starting in state 0 and
    ending up in that terminal state, and with the last slot containing the
    lowest common denominator between each terminal state's exact
    fraction probability.

    Example A:
        Input:
            (int) m = [[0, 2, 1, 0, 0],
                       [0, 0, 0, 3, 4],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]]
        Output:
            (int list) [7, 6, 8, 21]

    Example B:
        Input:
            (int) m = [[0, 1, 0, 0, 0, 1],
                       [4, 0, 0, 3, 2, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0]]
        Output:
            (int list) [0, 3, 2, 9, 14]

    Constraints and Assumptions:
    1) The matrix is at most 10 by 10. It should work for larger, but it has
    not been tested on larger so no guarantees.
    2) m is composed only of nonnegative ints.
    3) There is always an observed path from the current state to a terminal state.
    4) The denominator for last slot of the returned list will fits within
    a signed 32-bit integer during the calculation, as long as the fraction is
    simplified regularly.
    """
    canonical_form_info = get_canonical_form(m)
    T = canonical_form_info[0] # canonical form, floating point probabilities
    tr = canonical_form_info[1] # num of transition states
    tm = canonical_form_info[2] # num of terminal states

    # check if we can end early
    if canonical_form_info[3]:
        # zero is terminal, add other terminals at 0 prob if necessary
        probabilities = [1]
        for x in range(tm-1):
            probabilities.append(0)
        probabilities.append(1)
        return probabilities

    R = construct_R(T, tr, tm)  # subset of canonical form of T
    N = construct_N(T, tr)  # fundamental form of T
    B = standard_matrix_product(N, R)  # probabilities of ending in each
    # terminal state when starting from each transition state

    # return formatted probabilities of ending in each terminal starting from 0
    return format_terminal_probabilities(B, 0)

# helpers


def format_terminal_probabilities(B, transition_state):
    """Format and return probabilities for ending in each terminal state when
    starting from a particular state within an Absorbing Markov Chain.

    Arguments:
        B -- the list of lists of floats where B[i][j] is the probability of
        ending in state j when starting from i for an Absorbing Markov Chain
        transition_state -- the transition state to start from
    Return:
        A list of ints with the first numberOfTerminalStates slots containing
        the numerator of the exact fraction probability of starting in state
        transition_state ending up in that terminal state, and with the last
        slot containing the lowest common denominator between each terminal
        state's exact fraction probability
    """
    terminal_probabilities = B[transition_state]
    tm = len(terminal_probabilities)
    lcm = 1
    for state in range(tm):
        terminal_probabilities[state] = fractions.Fraction(terminal_probabilities[state]).limit_denominator()
        if terminal_probabilities[state] != 0:
            if state == 1:
                lcm = terminal_probabilities[state].denominator
            if state >= 1:
                lcm = get_lcm(lcm, terminal_probabilities[state].denominator)

    for state in range(tm):
        terminal_probabilities[state] = terminal_probabilities[state].numerator * lcm / terminal_probabilities[state].denominator
    terminal_probabilities.append(lcm)
    return terminal_probabilities

def construct_R(T, tr, tm):
    """Construct R, the top-right quadrant of the canonical form T of
    an Absorbing Markov Chain.

    R is nonzero and R[i][j] gives the probability of moving from
    transition state i to terminal state j.

    Arguments:
        T -- the canonical form of an Absorbing Markov Chain, as
            as list of lists of floats
        tr -- int, the number of transition states in T
        tm -- int, the number of terminal states in T
    Return:
        R of T, as a list of lists of floats
    """
    R = []
    for row in range(tr):
        R.append([])
        for col in range(len(T)-tm, len(T)):
            R[row].append(T[row][col])

    return R


def construct_N(T, tr):
    """Construct the fundamental matrix N from the canonical form T of
    an Absorbing Markov Chain.

    N[i][j] gives the expected number of times the chain is in state j
    given that the chain started in state i.

    Arguments:
        T -- the transition matrix for the Absorbing Markov Chain
            represented as a list of lists of floats
        tr -- an int representing the number of transition states
            in T
    Return:
        The fundamental matrix of T, as a list of lists of floats
    """
    I = [[0]*tr for x in range(tr)]
    for x in range(tr):
        I[x][x] = 1
    IminusQ = []
    for row in range(tr):
        IminusQ.append([])
        for col in range(tr):
            IminusQ[row].append(I[row][col] - T[row][col])

    return invert(IminusQ)


def invert(A):
    """Returns the inverse of A, where  A is a square matrix in the form
    of a nested list of lists.
    Thanks to Alphanumeric Sheep Pig at:
    http://www.alphasheep.co.za/2015/06/on-matrix-inversion-in-python.html"""
    A = [A[i]+[int(i==j) for j in range(len(A))] for i in range(len(A))]
    for i in range(len(A)):
        A[i:] = sorted(A[i:], key=lambda r: -abs(r[i]))
        A[i] = [A[i][j]/A[i][i] for j in range(len(A)*2)]
        A = [[A[j][k] if i==j else A[j][k]-A[i][k]*A[j][i] for \
              k in range(len(A)*2)] for j in range(len(A))]
    return [A[i][-len(A):] for i in range(len(A))]


def standard_matrix_product(A, B):
    """Multiply matrix A by matrix B and return the result"""
    rows = len(A)
    cols = len(B[0])
    result = [[0]*cols for x in range(rows)]

    # iterate through rows of A
    for i in range(rows):
        # iterate through columns of B
        for j in range(cols):
            # iterate through rows of B
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]

    return result


def get_lcm(x, y):
    """Return the least common multiple of x and y.
    Works by first getting the greatest common divisor."""
    return x * y / get_gcd(x, y)


def get_gcd(x, y):
    """Return the greatest common divisor or x and y"""
    while y != 0:
       z = y
       y = x % y
       x = z
    return x


def get_canonical_form(matrix):
    """Return the canonical form and related info for the given matrix
    representing an Absorbing Markov Chain.

    Note that the argument matrix does not have probabilities, but rather
    ints showing a sampling with the number of times each state has
    transitioned to other states.

    Also note that re-ordering of the states may occur, but that relative
    order of transition states and terminal states remains constant.
    That is, if Si and Sj are both terminal or transitional, their
    relative ordering will hold from observation matrix -> canonical form.
    But, if one Si and Sj is terminal and one is transitional, their relative
    ordering may not hold from observation matrix -> canonical form.

    Arguments:
        matrix -- a list of lists of ints where matrix[i][j] is the number
            of times state i has been observed transitioning to state j
    Return:
        A 4-length tuple with the following entries:
         tuple[0] -- the canonical form as a list of lists of floats where
            tuple[0][i][j] is the observed probability that state i will
            transition to state j
         tuple[1] -- int, the number of transition states
         tuple[2] -- int, the number of terminal states
         tuple[3] -- boolean, true if state 0 is a terminal state,
            false otherwise
    """
    T_with_old = []
    transitions = []
    terminals = []
    old_to_new = {}
    zero_is_term = False

    for state in range(len(matrix)):
        is_transition = False
        this_state = (state, [])
        state_total = 0
        for trans in range(len(matrix)):
            state_total += matrix[state][trans]
            if matrix[state][trans] > 0 and state != trans:
                is_transition = True
        if is_transition:
            for trans in range(len(matrix)):
                this_state[1].append(matrix[state][trans] / float(state_total))
            transitions.append(this_state)
        else:
            if state == 0:
                zero_is_term = True
            for trans in range(len(matrix)):
                if this_state[0] == trans:
                    this_state[1].append(1)
                else:
                    this_state[1].append(0)
            terminals.append(this_state)

    tr = len(transitions)
    tm = len(terminals)

    # append the states in the correct order, making note of their old -> new numbers
    for stateNum in range(tr):
        old_to_new[transitions[stateNum][0]] = stateNum
        T_with_old.append(transitions[stateNum])
    for stateNum in range(tm):
        old_to_new[terminals[stateNum][0]] = stateNum + tr
        T_with_old.append(terminals[stateNum])

    T = [[0]*len(matrix) for i in range(len(matrix))]
    # update T based on the old -> new numbers
    for state in range(len(matrix)):
        for trans in range(len(matrix)):
            T[state][old_to_new[trans]] = T_with_old[state][1][trans]

    return (T, tr, tm, zero_is_term)

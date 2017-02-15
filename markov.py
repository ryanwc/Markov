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
    transition_info = get_transition_matrix_info(m)
    T = transition_info[0] # canonical form, floating point probabilities
    tr = transition_info[1] # num of transition states
    tm = transition_info[2] # num of terminal states

    # check if we can end early
    if transition_info[3]:
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


def get_transition_matrix_info(matrix):
    """Get the transition matrix and related info for the given
    2D matrix.
    of matrix[state1][state2] = observed times Runs in n^2 time.
    Returns tuple of one matrix and two integers
    Matrix has transition states as first rows
    (Transition matrix, num transition states, num absorbtion states)"""
    tm = 0
    tr = 0
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

# tests
# to-do: convert to unit tests

drunk_ex = [[0, 0, 0, 1, 0], [1, 0, 1, 0, 0], [0, 1, 0, 0, 1], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0]]
ex_one = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
ex_twoA = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
ex_twoB = [[0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [4, 2, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0]]
ex_twoC = [[0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [4, 2, 3, 0, 0, 0]]
ex_one_term = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
ex_one_with_unreach = [[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
ex_one_with_unreach2 = [[0, 0, 0, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], [0, 0, 0, 0, 0]]
ex_zero_term_more_term = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
ex_zero_term_unreach_tr = [[1,0,0,0,0,2,0,4,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0,0],[0,0,0,3,0,0,5,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]] # should be two terminals, but zero0
print "--------------------------"
drunk_ans = answer(drunk_ex)
print 'drunk_ans is', drunk_ans
print "--------------------------"
ans_one = answer(ex_one)
print 'ex_one is', ans_one
print "--------------------------"
ans_twoA = answer(ex_twoA)
print 'ex_twoA is', ans_twoA
print "--------------------------"
ans_twoB = answer(ex_twoB)
print 'ex_twoB is', ans_twoB
print "--------------------------"
ans_twoC = answer(ex_twoC)
print 'ex_twoC is', ans_twoC
print "--------------------------"
ans_one_term = answer(ex_one_term)
print 'ex_one_term is', ans_one_term
print "--------------------------"
ans_one_with_unreach = answer(ex_one_with_unreach)
print 'ex_one_with_unreach is', ans_one_with_unreach
print "--------------------------"
ans_one_with_unreach2 = answer(ex_one_with_unreach2)
print 'ex_one_with_unreach2 is', ans_one_with_unreach2
print "--------------------------"
ans_zero_term_more_term = answer(ex_zero_term_more_term)
print 'ex_zero_term_more_term is', ans_zero_term_more_term
print "--------------------------"
ans_zero_term_unreach_tr = answer(ex_zero_term_unreach_tr)
print 'ex_zero_term_unreach_tr is', ans_zero_term_unreach_tr
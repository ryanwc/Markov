import fractions


def answer(m):

    # construct T, the transition matrix of the given matrix
    # note, T has floating points representing probabilities
    transition_info = get_transition_matrix_info(m)
    T = transition_info[0]
    tr = transition_info[1]
    tm = transition_info[2]

    if transition_info[3]:
        # zero is terminal, add other terminals at 0 if necessary
        # avoids unnecessarily calculating absorptions probabilities
        probabilities = [1]
        for x in range(tm-1):
            probabilities.append(0)
        probabilities.append(1)
        return probabilities

    # construct R, the probabilities of transitions -> terminals
    # where R = firs tr rows of T and last tm columns of T
    R = []
    for row in range(tr):
        R.append([])
        for col in range(len(T)-tm, len(T)):
            R[row].append(T[row][col])

    # construct N, fundamental matrix of T
    # where N = [identity matrix - (Q = first tr rows and tr cols of T)] ^ -1
    N = []
    I = [[0]*tr for x in range(tr)]
    for x in range(tr):
        I[x][x] = 1
    IminusQ = []
    for row in range(tr):
        IminusQ.append([])
        for col in range(tr):
            IminusQ[row].append(I[row][col] - T[row][col])

    N = invert(IminusQ) # not giving right answer

    # multiply N by R to get probabilities of ending in each terminal state
    # when starting from each transition state
    B = standard_matrix_product(N, R)

    # construct list of integer probabilities when starting from state 0
    B0 = B[0]
    lcm = 1
    for state in range(tm):
        B0[state] = fractions.Fraction(B0[state]).limit_denominator()
        if B0[state] != 0:
            if state == 1:
                lcm = B0[state].denominator
            if state >= 1:
                lcm = get_lcm(lcm, B0[state].denominator)

    for state in range(tm):
        B0[state] = B0[state].numerator * lcm / B0[state].denominator
    B0.append(lcm)

    return B0

# helpers


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
    """Multiply matrix A by matrix B"""
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
    """Get least common multiple of x and y.
    Works by first getting the greatest common divisor."""
    return x * y / get_gcd(x, y)


def get_gcd(x, y):
    """Get greatest common divisor or x and y"""
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
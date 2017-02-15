import Queue



def standardMatrixProduct(A, B):
    n = len(A)
    C = [[0 for i in xrange(n)] for j in xrange(n)]
    for i in xrange(n):
        for j in xrange(n):
            for k in xrange(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

"""
def answer(board):

    '''
    - from current state, do bfs:
	- if state goes to state already reached before:
		- for this state:
			newCountCircularChoice -= countCircularChoice*probability
		- circularityProb = newCountCircularChoice / currStateTotal
		- for already reached state:
			newCountCircular += countCircularChoice*circularityProb
			countOthers -= countOther*(circularityProb/numOthers)
    - calculate terminal probabilities based on new counts
    '''

    # directed cyclic graph

    # normalize circular choices
    curr_state = 0
    curr_prob = 1
    q = Queue.Queue()
    q.put((curr_state, curr_prob))
    processed_states = {}
    terminals = []
    possible_states = {}

    state_with_prob = None
    while q.not_empty():

        state_with_prob = q.get()
        curr_state = state_with_prob[0]

        if curr_state in processed_states:
            continue

        curr_prob = state_with_prob[1]
        processed_states[curr_state] = True
        possible_states[curr_state] = {}

        total_count = sum(board[curr_state])

        for stateInd in range(len(board[curr_state])):

            # add all of the possible states from this state
            if curr_state[stateInd] > 0:
                possible_states[curr_state][stateInd] = True
                q.put((curr_state[stateInd], ))

                # if we can go to it and we already went there, circular
                if curr_state[stateInd] in processed_states:

                    curr_state[stateInd] -= curr_state[stateInd] * curr_prob
                    circularityProb = currState.transitions[state] / currState.total_transitions

                    # find circular choice by following parents
                    state.transitions[circularChoice] -= state.transitions[circularChoice] * circulatiryProb
                    state.transitions[each
                    not circularChoice] += state.transitions[not circularChoice] * circularityProp / numNotCicularChoices
                    # need to handle case of 100 % circular

    # calculate terminal probabilities

'''
    [0, 1, 0, 0, 0, 1],
	[4, 0, 0, 3, 2, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0]]
'''
"""
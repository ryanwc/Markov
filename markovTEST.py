import unittest
from markov import answer


def main():

    tests = MarkovTest()
    tests.test_drunk_walk()
    tests.test_googleA()
    tests.test_googleB()
    tests.test_reordering()
    tests.test_one_term()
    tests.test_two_term_one_unreach()
    tests.test_zero_is_term()


class MarkovTest(unittest.TestCase):

    def test_drunk_walk(self):

        drunk_ex = [[1, 0, 0, 0, 0], [1, 0, 1, 0, 0], [0, 1, 0, 1, 0], [0, 0, 1, 0, 1], [0, 0, 0, 0, 1]]
        drunk_ans = answer(drunk_ex)
        self.assertEquals([1, 0, 1], drunk_ans)

    def test_googleA(self):

        ex_one = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        ans_one = answer(ex_one)
        self.assertEquals([7, 6, 8, 21], ex_one)

    def test_googleB(self):

        ex_twoA = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0]]
        ans_twoA = answer(ex_twoA)
        self.assertEquals([0, 3, 2, 9, 14], ex_twoA)

    def test_reordering(self):

        ex_twoA = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0]]
        ex_twoB = [[0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [4, 2, 0, 3, 0, 0],
                   [0, 0, 0, 0, 0, 0]]
        ex_twoC = [[0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                   [4, 2, 3, 0, 0, 0]]

        ans_twoA = answer(ex_twoA)
        ans_twoB = answer(ex_twoB)
        ans_twoC = answer(ex_twoC)

        self.assertEquals([0, 3, 2, 9, 14], ans_twoA)
        self.assertEquals([2, 0, 3, 9, 14], ans_twoB)
        self.assertEquals([2, 3, 0, 9, 14], ans_twoC)

    def test_one_term(self):

        ex_one_term = [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
        ans_one_term = answer(ex_one_term)
        self.assertEquals([1, 1], ans_one_term)

    def test_two_term_one_unreach(self):

        ex_one_with_unreach = [[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        ans_one_with_unreach = answer(ex_one_with_unreach)
        self.assertEquals([1, 0, 1], ans_one_with_unreach)

    def test_zero_is_term(self):

        ex_zero_term_more_term = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        ans_zero_term_more_term = answer(ex_zero_term_more_term)
        self.assertEquals([1, 0, 0, 0, 1], ans_zero_term_more_term)


if __name__ == '__main__':
    unittest.main()

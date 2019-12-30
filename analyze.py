"""
Copyright 2019, University of Freiburg,
Chair of Algorithms and Data Structures.
Author: Hannah Bast <bast@cs.uni-freiburg.de>
"""

import sys
import math


# Usage info printed when calling script without arguments.
usage_info = """
Usage: python3 analyze.py <score type>

Analyze the similarity of the rankings produced by the two PCs, where
<score type> specifies which score is used for each submission and PC:

av :   confidence-weighted average scores of the reviewers
l5 :   single-submission score from {+2, +1, 0, -1, -2}
l3 :   l5-score with +2, +1 -> +1 and 0 -> 0 and -1, -2 -> -1
av5:   av scores, rounded to nearest score from {+2, +1, 0, -1, -2}
av3:   av5 scores, reduced to {+1, 0, -1} like l5 -> l3
avr:   random average score (NYI)
l5r:   random l5 score (NYI)
l3r:   random l3 score(NYI)
"""

# Dictionary with long names for the score types above.
score_type_names = {"av": "average score",
                    "l5": "single-submission score from {-2,-1,0,+1,+2}",
                    "l3": "single-submission score from {-1,0,+1}",
                    "av5": "av score, rounded to nearest l5 score",
                    "av3": "obtainde from av5 score, like l3 from l5"}


class EsaExperimentData:

    def __init__(self):
        """
        The variable all_scores contains one list of score-confidence pairs for
        each PC and phase. Will be filled by read_all_score_files.
        """

        self.all_scores = [[[], []], [[], []], [[], []]]

    def read_score_file(self, file_name):
        """
        Read score file (with six or eight columns) and return a list of the
        confidence-weighted averages and the single submission scores (see
        function single_submission_score below), one of each of them for each
        row in the input file.

        Note that the scores are read as floats, because the fifth column
        (which, if it exists, is the PC score = average score from a vote). The
        confidences are always integers.

        TODO: signal an error if one of the first six columns is empty.

        >>> with open("test.tsv", "w+") as f:
        ...     print("+1 4 -1 3 +0 3 __ _", file = f)
        ...     print("+0 4 -1 2 +0 2 -1 4", file = f)
        ...     print("+3 2 -2 5 +0 3 -1 2 -1 5", file = f)
        >>> ee = EsaExperimentData()
        >>> ee.read_score_file("test.tsv") # doctest: +NORMALIZE_WHITESPACE
        [[(1.0, 4), (-1.0, 3), (0.0, 3)],
         [(0.0, 4), (-1.0, 2), (0.0, 2), (-1.0, 4)],
         [(3.0, 2), (-2.0, 5), (0.0, 3), (-1.0, 2), (-1.0, 5)]]
        """

        all_scores = []
        with open(file_name) as f:
            for line in f:
                entries = line.rstrip().split(" ")
                scores = list(map(float, entries[0:5:2]))
                confis = list(map(int, entries[1:6:2]))

                # Add score and confidence from columns 7 and 8 if non-empty
                # and from columns 9 and 10 if they exist.
                assert len(entries) >= 8, entries
                if entries[7].isdigit():
                    scores.append(float(entries[6]))
                    confis.append(int(entries[7]))
                if len(entries) == 10:
                    scores.append(float(entries[8]))
                    confis.append(int(entries[9]))

                all_scores.append(list(zip(scores, confis)))
        return all_scores

    def read_all_score_files(self):
        """
        Read the six score files (one of each of the two PC and for one of the
        three phases) and remember them.

        The test cases below make a simple sanity check by testing whether the
        averages (which were also computed in a separate spreadsheet) are
        alright.

        >>> ee = EsaExperimentData()
        >>> ee.read_all_score_files()
        >>> avg_scores = [[[], []], [[], []], [[], []]]
        >>> avg_scores[0][0] = ee.compute_scores(ee.all_scores[0][0], "av")
        >>> avg_scores[0][1] = ee.compute_scores(ee.all_scores[0][1], "av")
        >>> avg_scores[1][0] = ee.compute_scores(ee.all_scores[1][0], "av")
        >>> avg_scores[1][1] = ee.compute_scores(ee.all_scores[1][1], "av")
        >>> avg_scores[2][0] = ee.compute_scores(ee.all_scores[2][0], "av")
        >>> avg_scores[2][1] = ee.compute_scores(ee.all_scores[2][1], "av")
        >>> ["%.2f" % x for x in avg_scores[0][0]] # doctest:+ELLIPSIS
        ['2.00', '2.00', '2.00', ..., '-1.62', '-2.00', '-2.00']
        >>> ["%.2f" % x for x in avg_scores[0][1]] # doctest:+ELLIPSIS
        ['0.90', '2.00', '2.00', ..., '-2.00', '-1.30', '-2.00']
        >>> ["%.2f" % x for x in avg_scores[1][0]] # doctest:+ELLIPSIS
        ['2.00', '2.00', '2.00', ..., '-2.00', '-2.00', '-2.00']
        >>> ["%.2f" % x for x in avg_scores[1][1]] # doctest:+ELLIPSIS
        ['1.30', '2.00', '2.00', ..., '-2.00', '-1.30', '-2.00']
        >>> ["%.2f" % x for x in avg_scores[2][0]] # doctest:+ELLIPSIS
        ['1.97', '2.00', '2.00', ..., '-2.00', '-2.00', '-2.00']
        >>> ["%.2f" % x for x in avg_scores[2][1]] # doctest:+ELLIPSIS
        ['1.21', '2.00', '2.00', ..., '-2.00', '-1.30', '-2.00']
        """

        self.all_scores[0][0] = self.read_score_file("scores-phase1-pc1.tsv")
        self.all_scores[0][1] = self.read_score_file("scores-phase1-pc2.tsv")
        self.all_scores[1][0] = self.read_score_file("scores-phase2-pc1.tsv")
        self.all_scores[1][1] = self.read_score_file("scores-phase2-pc2.tsv")
        self.all_scores[2][0] = self.read_score_file("scores-phase3-pc1.tsv")
        self.all_scores[2][1] = self.read_score_file("scores-phase3-pc2.tsv")

    def compute_scores(self, score_confidence_pairs, score_type):
        """
        Given a list of score-confidence pairs, compute a single score
        depending on the given type. See the usage_info string at the beginning
        of the file for the options, see the test cases for examples, and see
        the code for details.

        Since the functions below already provide extensive unit tests for each
        of the types, the following test cases are deliberately simple and
        only check that the output list has the right length and the right
        function was called.

        >>> ee = EsaExperimentData()
        >>> ee.compute_scores([[(+1, 3)], [(+2, 3)], [(+0, 4)]], "av")
        [1.0, 2.0, 0.0]
        >>> ee.compute_scores([[(+1, 3), (+2, 3), (+0, 4)]], "l5")
        [1]
        >>> ee.compute_scores([[(+1, 3)], [(+2, 3)], [(-2, 2)]], "l3")
        [0, 1, -1]
        >>> ee.compute_scores([[(+1, 3), (+2, 3), (+2, 3)]], "av5")
        [2]
        >>> ee.compute_scores([[(+1, 3), (+2, 3), (+2, 3)]], "av3")
        [1]
        """

        sc_pairs = score_confidence_pairs
        if score_type == "av":
            return list(map(self.average_score, sc_pairs))
        elif score_type == "l5":
            return list(map(self.l5_score, sc_pairs))
        elif score_type == "l3":
            l5tol3_map = {2:1, 1:1, 0:0, -1:-1, -2:-1}
            return list(map(lambda x: l5tol3_map[x],
                            self.compute_scores(sc_pairs, "l5")))
        if score_type == "av5":
            return list(map(lambda x: round(x), 
                            self.compute_scores(sc_pairs, "av")))
        if score_type == "av3":
            l5tol3_map = {2:1, 1:1, 0:0, -1:-1, -2:-1}
            return list(map(lambda x: l5tol3_map[x],
                            self.compute_scores(sc_pairs, "av5")))


    def average_score(self, score_confidence_pairs):
        """
        Compute the confidence-weighted average of the given scores.

        >>> ee = EsaExperimentData()
        >>> ee.average_score([(+1, 4), (-1, 3), (+0, 3)])
        0.1
        >>> ee.average_score([(+2, 4), (+0, 2), (+1, 2)])
        1.25
        >>> ee.average_score([(+0, 4), (-1, 2), (+0, 2), (-1, 4)])
        -0.5
        """

        return sum(x * y for x, y in score_confidence_pairs) \
            / sum(y for x, y in score_confidence_pairs)

    def l5_score(self, score_confidence_pairs):
        """
        Compute a single score form the range {+2, +1, 0, -1, -2} from the
        given score, confidence pairs. The rules are as follows, where a +2 and
        a -2 are only considered as such if the associated confidence is >= 3

        +2 : if all scores are +2
        +1 : if at least one score is +2
         0 : at least one +1, but no +2
        -1 : no +1 or +2, but no -2
        -2 : no +1 or +2, and at least one -2

        >>> ee = EsaExperimentData()
        >>> ee.l5_score([(+2, 3), (+2, 4), (+2, 5)])
        2
        >>> ee.l5_score([(+2, 3), (+2, 4), (+2, 2)])
        1
        >>> ee.l5_score([(+1, 5), (+1, 4), (+2, 3)])
        1
        >>> ee.l5_score([(+1, 2), (+0, 4), (+1, 4)])
        0
        >>> ee.l5_score([(+0, 3), (-1, 4), (-1, 2)])
        -1
        >>> ee.l5_score([(+0, 3), (-1, 4), (-2, 2)])
        -1
        >>> ee.l5_score([(+0, 3), (-1, 4), (-2, 3)])
        -2
        >>> ee.l5_score([(-2, 3), (+0, 4), (+0, 3)])
        -2
        """

        # Copy scores, but change +2 to +1 and -2 to -1 if confidence < 3. The
        # m in scores_m stands for modified.
        scores_m = list(map(
            lambda x, y: min(1, max(-1, x)) if abs(x) == 2 and y < 3 else x,
            *zip(*score_confidence_pairs)))
        if all(score == 2 for score in scores_m):
            return 2
        elif max(scores_m) == 2:
            return 1
        elif max(scores_m) == 1:
            return 0
        elif min(scores_m) > -2:
            return -1
        else:
            return -2

    def print_statistics(self, score_type):
        """
        Print statistics for the given score type. See the usage_info string at
        the beginning of this file for the options. See function compute_scores
        for the details of how the scores are computed for each type.
        """

        if score_type not in score_type_names:
            print()
            print("Score type \"%s\" does not exist or is not yet implemented"
                  % score_type)
            print(usage_info)
            sys.exit(1)
        score_type_name = score_type_names[score_type]
        print()
        print("\x1b[1mThe score type is: %s\x1b[0m" % score_type_name)

        scores = [[[], []], [[], []], [[], []]]
        scores[0][0] = self.compute_scores(self.all_scores[0][0], score_type)
        scores[0][1] = self.compute_scores(self.all_scores[0][1], score_type)
        scores[1][0] = self.compute_scores(self.all_scores[1][0], score_type)
        scores[1][1] = self.compute_scores(self.all_scores[1][1], score_type)
        scores[2][0] = self.compute_scores(self.all_scores[2][0], score_type)
        scores[2][1] = self.compute_scores(self.all_scores[2][1], score_type)

        print()
        print("Kendall tau (p / b / a) between PCs and phases:")
        print()
        tau_p_1a = kendall_tau_p(scores[0][0], scores[0][1])
        tau_p_2a = kendall_tau_p(scores[1][0], scores[1][1])
        tau_p_3a = kendall_tau_p(scores[2][0], scores[2][1])
        tau_a_1a = kendall_tau_a(scores[0][0], scores[0][1])
        tau_a_2a = kendall_tau_a(scores[1][0], scores[1][1])
        tau_a_3a = kendall_tau_a(scores[2][0], scores[2][1])
        tau_b_1a = kendall_tau_b(scores[0][0], scores[0][1])
        tau_b_2a = kendall_tau_b(scores[1][0], scores[1][1])
        tau_b_3a = kendall_tau_b(scores[2][0], scores[2][1])
        print("Phase 1: %.2f / %.2f / %.2f" % (tau_p_1a, tau_b_1a, tau_a_1a))
        print("Phase 2: %.2f / %.2f / %.2f" % (tau_p_2a, tau_b_2a, tau_a_2a))
        print("Phase 3: %.2f / %.2f / %.2f" % (tau_p_3a, tau_b_3a, tau_a_3a))
        print()
        tau_p_pc1_12a = kendall_tau_p(scores[0][0], scores[1][0])
        tau_p_pc1_23a = kendall_tau_p(scores[1][0], scores[2][0])
        tau_p_pc2_12a = kendall_tau_p(scores[0][1], scores[1][1])
        tau_p_pc2_23a = kendall_tau_p(scores[1][1], scores[2][1])
        tau_b_pc1_12a = kendall_tau_b(scores[0][0], scores[1][0])
        tau_b_pc1_23a = kendall_tau_b(scores[1][0], scores[2][0])
        tau_b_pc2_12a = kendall_tau_b(scores[0][1], scores[1][1])
        tau_b_pc2_23a = kendall_tau_b(scores[1][1], scores[2][1])
        tau_a_pc1_12a = kendall_tau_a(scores[0][0], scores[1][0])
        tau_a_pc1_23a = kendall_tau_a(scores[1][0], scores[2][0])
        tau_a_pc2_12a = kendall_tau_a(scores[0][1], scores[1][1])
        tau_a_pc2_23a = kendall_tau_a(scores[1][1], scores[2][1])
        print("PC1, Phases 1 <-> 2: %.2f / %.2f / %.2f"
              % (tau_p_pc1_12a, tau_b_pc1_12a, tau_a_pc1_12a))
        print("PC2, Phases 1 <-> 2: %.2f / %.2f / %.2f"
              % (tau_p_pc2_12a, tau_b_pc2_12a, tau_a_pc2_12a))
        print("PC1, Phases 2 <-> 3: %.2f / %.2f / %.2f"
              % (tau_p_pc1_23a, tau_b_pc1_23a, tau_a_pc1_23a))
        print("PC2, Phases 2 <-> 3: %.2f / %.2f / %.2f"
              % (tau_p_pc2_23a, tau_b_pc2_23a, tau_a_pc2_23a))
        print()


# Global functions

def kendall_tau_a(scores1, scores2):
    """
    Computes a distance measure based on variant A of the Kendall tau
    correlation.  This correlation is (nc - nd) / N, where nc is the number of
    concordant pairs, nd is the number of discordant pairs, and N = n * (n - 1)
    / 2 is the number of all pairs i, j with j < i (we could also consider all
    pairs i, j with i < j). A pair i, j is concordant if the relation between
    scores1[i] and scores2[j] and the relation between scores2[i] and
    scores2[j] are both < or both >. The pair is discordant if one relation is
    < and the other is >. If one or both relations are ==, the pair is counted
    as neither discordant nor concordant.

    The correlation is a number in the range [-1, 1]. We obtain a normalized
    distance in the range [0, 1] by taking (1 - correlation) / 2.

    When there are no ties, we have nc = N - nd and the correlation becomes
    1 - 2 * nd / N, and the distance is then simply nd / N.

    If there are many ties, this correlation is closer to 0 than for tau_a and
    tau_p versions below, where the demoninator is smaller. For a positive
    correlation, this means a larger distance.

    >>> kendall_tau_a([1, 2, 3, 4], [2, 3, 4, 5])
    0.0
    >>> kendall_tau_a([1, 2, 2, 4], [2, 3, 3, 5]) # doctest:+ELLIPSIS
    0.0833...
    >>> kendall_tau_a([1, 2, 3, 4], [2, 3, 3, 5]) # doctest:+ELLIPSIS
    0.0833...
    >>> kendall_tau_a([1, 2, 3, 4], [5, 3, 2, 1])
    1.0
    >>> kendall_tau_a([1, 2, 3, 4], [5, 3, 3, 1]) # doctest:+ELLIPSIS
    0.9166...
    >>> kendall_tau_a([1, 2, 2, 4], [5, 3, 3, 1]) # doctest:+ELLIPSIS
    0.9166...
    """

    num_discordant_pairs = 0
    num_concordant_pairs = 0
    assert len(scores1) == len(scores2)
    n = len(scores1)
    for i in range(n):
        for j in range(i):
            # Note that (x > y) - (x < y) = sign(x) in { -1, 0, +1 }
            cmp1 = (scores1[i] > scores1[j]) - (scores1[i] < scores1[j])
            cmp2 = (scores2[i] > scores2[j]) - (scores2[i] < scores2[j])
            if cmp1 * cmp2 == +1:
                num_concordant_pairs += 1
            if cmp1 * cmp2 == -1:
                num_discordant_pairs += 1
    num_all_pairs = n * (n - 1) / 2
    correlation = (num_concordant_pairs - num_discordant_pairs) / num_all_pairs
    return (1 - correlation) / 2


def kendall_tau_b(scores1, scores2):
    """
    Distance measure based on variant b of the Kendall tau correlation, which
    is computed as the ratio of num_concordant_pairs - num_discordant_pairs
    (nc - nd) divided by the geometric mean of the number of non-tied pairs in
    the first list (np1) and number of non-tied pairs in the second list (np2).

    The correlation is a number in the range [-1, 1]. From this, we compute
    the normalized distance as (1 - correlation) / 2, which is in [0, 1]. A
    perfect correlation of 1 than corresponds to a normalized distance of 0.

    Test case 1: nc = 6, nd = 0, np1 = np2 = 6
    >>> kendall_tau_b([1, 2, 3, 4], [2, 3, 4, 5])
    0.0

    Test case 2: nc = 5, nd = 0, np1 = np2 = 5
    >>> kendall_tau_b([1, 2, 2, 4], [2, 3, 3, 5])
    0.0

    Test case 3: nc = 5, nd = 0, np1 = 6, np2 = 5, 5/sqrt(30) = 0.9128...
    >>> kendall_tau_b([1, 2, 3, 4], [2, 3, 3, 5]) # doctest:+ELLIPSIS,
    0.04356...

    Test case 4: nc = 0, nd = 6, np1 = np2 = 6
    >>> kendall_tau_b([1, 2, 3, 4], [5, 3, 2, 1])
    1.0

    Test case 5: nc = 0, nd = 5, np1 = np2 = 5
    >>> kendall_tau_b([1, 2, 2, 4], [5, 3, 3, 1])
    1.0

    Test case 6: nc = 0, nd = 3, np1 = 6, np2 = 3, -3/sqrt(18) = -0.7071...
    >>> kendall_tau_b([1, 2, 3, 4], [5, 3, 3, 3]) # doctest:+ELLIPSIS
    0.8535...
    """

    # Compute the number of concordant and discordant pairs, as well as, for
    # each list, the number of index pairs without ties.
    assert len(scores1) == len(scores2)
    n = len(scores1)
    num_concordant_pairs = 0
    num_discordant_pairs = 0
    num_index_pairs_without_ties_1 = 0
    num_index_pairs_without_ties_2 = 0
    for i in range(n):
        for j in range(i):
            # Note that (x > y) - (x < y) = sign(x) in { -1, 0, +1 }
            cmp1 = (scores1[i] > scores1[j]) - (scores1[i] < scores1[j])
            cmp2 = (scores2[i] > scores2[j]) - (scores2[i] < scores2[j])
            if cmp1 * cmp2 == +1:
                num_concordant_pairs += 1
            if cmp1 * cmp2 == -1:
                num_discordant_pairs += 1
            if cmp1 != 0:
                num_index_pairs_without_ties_1 += 1
            if cmp2 != 0:
                num_index_pairs_without_ties_2 += 1
    correlation = ((num_concordant_pairs - num_discordant_pairs) /
                   math.sqrt(num_index_pairs_without_ties_1 *
                             num_index_pairs_without_ties_2))
    return (1 - correlation) / 2


def kendall_tau_p(scores1, scores2, p=0.50):
    """
    Compute the p-normalized Kendall Tau as described in Fagin et al.:
    Comparing and Aggregating Rankings with Ties, PODS 2004
    https://dl.acm.org/citation.cfm?id=1055568

    For each pair i, j with i < j compare the order of scores1[i] and
    scores1[j] with the order of the ranks of scores2[i] and scores2[j]. If the
    order is the same, there is no penalty. If the order is opposite, there is
    a penalty of one. If the ranks are the same for exactly one of the score
    lists, the penalty is p (default 0.5).

    The result is then simply the average of these penalties. This is different
    from the definition in the paper above, where a weighted average is taken.
    (The weights are all 1, except for the pairs with a tie in the ground
    truth, where the weight is 0.5. Note that this is asymmetric, which makes
    sense when you have a ground truth, but not in our setting.)

    In the first test case, the ranking is the same. In the second test
    case, there are three pairs, all transposed. In the third test case, there
    are six pairs and the order is the same for five of them and for exactly
    one pair (comparing the scores at indices 1 and 2), the penalty is 0.5

    >>> kendall_tau_p([1, 2, 3], [4, 5, 6])
    0.0
    >>> kendall_tau_p([1, 2, 3], [6, 5, 4])
    1.0
    >>> kendall_tau_p([4, 2, 3, 1], [3, 2, 2, 1]) # doctest:+ELLIPSIS
    0.08703...
    >>> kendall_tau_p([3, 2, 2, 1], [4, 2, 3, 1]) # doctest:+ELLIPSIS
    0.08703...
    """

    assert len(scores1) == len(scores2)
    n = len(scores1)
    num_discordant_pairs = 0.0
    # Count the number of discordant pairs, where pairs which are tied in the
    # one list and different in the other count p (default 0.5, see above).
    num_pairs_1 = 0.0
    num_pairs_2 = 0.0
    for i in range(n):
        for j in range(i):
            # Note that (x > y) - (x < y) = sign(x) in { -1, 0, +1 }
            cmp1 = (scores1[i] > scores1[j]) - (scores1[i] < scores1[j])
            cmp2 = (scores2[i] > scores2[j]) - (scores2[i] < scores2[j])
            if cmp1 * cmp2 == +1:
                num_pairs_1 += 1
                num_pairs_2 += 1
            elif cmp1 * cmp2 == -1:
                num_discordant_pairs += 1
                num_pairs_1 += 1
                num_pairs_2 += 1
            elif cmp1 != 0 or cmp2 != 0:
                num_discordant_pairs += p
                if cmp1 == 0:
                    # cmp1 == 0, cmp2 != 0
                    num_pairs_1 += p
                    num_pairs_2 += 1
                else:
                    # cmp1 != 0, cmp2 == 0
                    num_pairs_1 += 1
                    num_pairs_2 += p
            else:
                # cmp1 == 0, cmp2 == 0
                num_pairs_1 += 0
                num_pairs_2 += 0
    # Return the average penalty.
    return num_discordant_pairs / math.sqrt(num_pairs_1 * num_pairs_2)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1].endswith("help"):
        print(usage_info)
        sys.exit(1)
    score_type = sys.argv[1]
    ee = EsaExperimentData()
    ee.read_all_score_files()
    ee.print_statistics(score_type)

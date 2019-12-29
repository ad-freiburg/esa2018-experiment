"""
Copyright 2019, University of Freiburg,
Chair of Algorithms and Data Structures.
Author: Hannah Bast <bast@cs.uni-freiburg.de>
"""

import math


class EsaExperimentData:

    def __init__(self):
        """ Constructor. """

        self.avg_scores = [[[], []], [[], []], [[], []]]
        self.sgl_scores = [[[], []], [[], []], [[], []]]

    def read_score_file(self, file_name):
        """
        Read score file (with six or eight columns) and return a list of the
        confidence-weighted averages and the single submission scores (see
        function single_submission_score below), one of each of them for each
        row in the input file.
        
        TODO: signal an error if one of the first six columns is empty.

        >>> with open("test.tsv", "w+") as f:
        ...     print("+1 4 -1 3 +0 3 __ _", file = f)
        ...     print("+2 4 +0 2 +1 2 __ _", file = f)
        ...     print("+0 4 -1 2 +0 2 -1 4", file = f)
        >>> ee = EsaExperimentData()
        >>> ee.read_score_file("test.tsv")
        ([0.1, 1.25, -0.5], [0, 1, -1])
        """

        avg_scores = []
        sgl_scores = []
        with open(file_name) as f:
            for line in f:
                entries = line.rstrip().split(" ")
                scores = list(map(float, entries[0:5:2]))
                confis = list(map(float, entries[1:6:2]))

                # Add score and confidence from columns 7 and 8 if non-empty
                # and from columns 9 and 10 if they exist.
                assert len(entries) >= 8, entries
                if entries[7].isdigit():
                    scores.append(float(entries[6]))
                    confis.append(float(entries[7]))
                if len(entries) == 10:
                    scores.append(float(entries[8]))
                    confis.append(float(entries[9]))

                average = sum(x * y for x, y in zip(scores, confis)) \
                    / sum(confis)

                avg_scores.append(average)
                sgl_scores.append(single_submission_score(scores, confis))
        return avg_scores, sgl_scores

    def read_all_score_files(self):
        """
        Read all the score files and store the list of scores for Phase k and
        PC i in self.avg_scores[k][i]

        >>> ee = EsaExperimentData()
        >>> ee.read_all_score_files()
        >>> ["%.2f" % x for x in ee.avg_scores[0][0]] # doctest:+ELLIPSIS
        ['2.00', '2.00', '2.00', ..., '-1.62', '-2.00', '-2.00']
        >>> ["%.2f" % x for x in ee.avg_scores[0][1]] # doctest:+ELLIPSIS
        ['0.90', '2.00', '2.00', ..., '-2.00', '-1.30', '-2.00']
        >>> ["%.2f" % x for x in ee.avg_scores[1][0]] # doctest:+ELLIPSIS
        ['2.00', '2.00', '2.00', ..., '-2.00', '-2.00', '-2.00']
        >>> ["%.2f" % x for x in ee.avg_scores[1][1]] # doctest:+ELLIPSIS
        ['1.30', '2.00', '2.00', ..., '-2.00', '-1.30', '-2.00']
        >>> ["%.2f" % x for x in ee.avg_scores[2][0]] # doctest:+ELLIPSIS
        ['1.97', '2.00', '2.00', ..., '-2.00', '-2.00', '-2.00']
        >>> ["%.2f" % x for x in ee.avg_scores[2][1]] # doctest:+ELLIPSIS
        ['1.21', '2.00', '2.00', ..., '-2.00', '-1.30', '-2.00']
        """

        self.avg_scores[0][0], self.sgl_scores[0][0] = \
                self.read_score_file("scores-phase1-pc1.tsv")
        self.avg_scores[0][1], self.sgl_scores[0][1] = \
                self.read_score_file("scores-phase1-pc2.tsv")
        self.avg_scores[1][0], self.sgl_scores[1][0] = \
                self.read_score_file("scores-phase2-pc1.tsv")
        self.avg_scores[1][1], self.sgl_scores[1][1] = \
                self.read_score_file("scores-phase2-pc2.tsv")
        self.avg_scores[2][0], self.sgl_scores[2][0] = \
                self.read_score_file("scores-phase3-pc1.tsv")
        self.avg_scores[2][1], self.sgl_scores[2][1] = \
                self.read_score_file("scores-phase3-pc2.tsv")

    def print_all_kendall_tau(self):
        """
        Print the Kendall tau between the rankings of the two PCs for all
        three phases.
        """

        print()
        print("Kendall tau (p / b / a) between PCs and phases (average scores):")
        print()
        tau_p_1a = kendall_tau_p(self.avg_scores[0][0], self.avg_scores[0][1])
        tau_p_2a = kendall_tau_p(self.avg_scores[1][0], self.avg_scores[1][1])
        tau_p_3a = kendall_tau_p(self.avg_scores[2][0], self.avg_scores[2][1])
        tau_a_1a = kendall_tau_a(self.avg_scores[0][0], self.avg_scores[0][1])
        tau_a_2a = kendall_tau_a(self.avg_scores[1][0], self.avg_scores[1][1])
        tau_a_3a = kendall_tau_a(self.avg_scores[2][0], self.avg_scores[2][1])
        tau_b_1a = kendall_tau_b(self.avg_scores[0][0], self.avg_scores[0][1])
        tau_b_2a = kendall_tau_b(self.avg_scores[1][0], self.avg_scores[1][1])
        tau_b_3a = kendall_tau_b(self.avg_scores[2][0], self.avg_scores[2][1])
        print("Phase 1: %.2f / %.2f / %.2f" % (tau_p_1a, tau_b_1a, tau_a_1a))
        print("Phase 2: %.2f / %.2f / %.2f" % (tau_p_2a, tau_b_2a, tau_a_2a))
        print("Phase 3: %.2f / %.2f / %.2f" % (tau_p_3a, tau_b_3a, tau_a_3a))
        print()
        tau_p_pc1_12a = kendall_tau_p(self.avg_scores[0][0], self.avg_scores[1][0])
        tau_p_pc1_23a = kendall_tau_p(self.avg_scores[1][0], self.avg_scores[2][0])
        tau_p_pc2_12a = kendall_tau_p(self.avg_scores[0][1], self.avg_scores[1][1])
        tau_p_pc2_23a = kendall_tau_p(self.avg_scores[1][1], self.avg_scores[2][1])
        tau_b_pc1_12a = kendall_tau_b(self.avg_scores[0][0], self.avg_scores[1][0])
        tau_b_pc1_23a = kendall_tau_b(self.avg_scores[1][0], self.avg_scores[2][0])
        tau_b_pc2_12a = kendall_tau_b(self.avg_scores[0][1], self.avg_scores[1][1])
        tau_b_pc2_23a = kendall_tau_b(self.avg_scores[1][1], self.avg_scores[2][1])
        print("PC1, Phases 1 <-> 2: %.2f / %.2f" % (tau_p_pc1_12a, tau_b_pc1_12a))
        print("PC2, Phases 1 <-> 2: %.2f / %.2f" % (tau_p_pc2_12a, tau_b_pc2_12a))
        print("PC1, Phases 2 <-> 3: %.2f / %.2f" % (tau_p_pc1_23a, tau_b_pc1_23a))
        print("PC2, Phases 2 <-> 3: %.2f / %.2f" % (tau_p_pc2_23a, tau_b_pc2_23a)) 
        print()

        print()
        print("Kendall tau (p / b / a) between PCs and phases (5-point scores):")
        print()
        tau_p_1s = kendall_tau_p(self.sgl_scores[0][0], self.sgl_scores[0][1])
        tau_p_2s = kendall_tau_p(self.sgl_scores[1][0], self.sgl_scores[1][1])
        tau_p_3s = kendall_tau_p(self.sgl_scores[2][0], self.sgl_scores[2][1])
        tau_a_1s = kendall_tau_a(self.sgl_scores[0][0], self.sgl_scores[0][1])
        tau_a_2s = kendall_tau_a(self.sgl_scores[1][0], self.sgl_scores[1][1])
        tau_a_3s = kendall_tau_a(self.sgl_scores[2][0], self.sgl_scores[2][1])
        tau_b_1s = kendall_tau_b(self.sgl_scores[0][0], self.sgl_scores[0][1])
        tau_b_2s = kendall_tau_b(self.sgl_scores[1][0], self.sgl_scores[1][1])
        tau_b_3s = kendall_tau_b(self.sgl_scores[2][0], self.sgl_scores[2][1])
        print("Phase 1: %.2f / %.2f / %.2f" % (tau_p_1s, tau_b_1s, tau_a_1s))
        print("Phase 2: %.2f / %.2f / %.2f" % (tau_p_2s, tau_b_2s, tau_a_2s))
        print("Phase 3: %.2f / %.2f / %.2f" % (tau_p_3s, tau_b_3s, tau_a_3s))
        print()
        tau_p_pc1_12s = kendall_tau_p(self.sgl_scores[0][0], self.sgl_scores[1][0])
        tau_p_pc1_23s = kendall_tau_p(self.sgl_scores[1][0], self.sgl_scores[2][0])
        tau_p_pc2_12s = kendall_tau_p(self.sgl_scores[0][1], self.sgl_scores[1][1])
        tau_p_pc2_23s = kendall_tau_p(self.sgl_scores[1][1], self.sgl_scores[2][1])
        tau_b_pc1_12s = kendall_tau_b(self.sgl_scores[0][0], self.sgl_scores[1][0])
        tau_b_pc1_23s = kendall_tau_b(self.sgl_scores[1][0], self.sgl_scores[2][0])
        tau_b_pc2_12s = kendall_tau_b(self.sgl_scores[0][1], self.sgl_scores[1][1])
        tau_b_pc2_23s = kendall_tau_b(self.sgl_scores[1][1], self.sgl_scores[2][1])
        print("PC1, Phases 1 <-> 2: %.2f / %.2f" % (tau_p_pc1_12s, tau_b_pc1_12s))
        print("PC2, Phases 1 <-> 2: %.2f / %.2f" % (tau_p_pc2_12s, tau_b_pc2_12s))
        print("PC1, Phases 2 <-> 3: %.2f / %.2f" % (tau_p_pc1_23s, tau_b_pc1_23s))
        print("PC2, Phases 2 <-> 3: %.2f / %.2f" % (tau_p_pc2_23s, tau_b_pc2_23s)) 

        print()

# Global functions

def single_submission_score(scores, confis):
    """
    Compute a single score for a submission, given the individual scores with
    confidences from the reviewers. The rules are as follows, where a +2 and a
    -2 are only considered as such if the associated confidence is >= 3

    +2 : if all scores are +2
    +1 : if at least one score is +2
     0 : at least one +1, but no +2
    -1 : no +1 or +2, but no -2
    -2 : no +1 or +2, and at least one -2

    >>> single_submission_score([+2, +2, +2], [3, 4, 5])
    2
    >>> single_submission_score([+2, +2, +2], [3, 4, 2])
    1
    >>> single_submission_score([+1, -1, +2], [5, 4, 3])
    1
    >>> single_submission_score([+1, +0, -1], [2, 4, 4])
    0
    >>> single_submission_score([+0, -1, -1], [3, 4, 2])
    -1
    >>> single_submission_score([+0, -1, -2], [3, 4, 2])
    -1
    >>> single_submission_score([+0, -1, -2], [3, 4, 3])
    -2
    >>> single_submission_score([-2, +0, +0], [3, 4, 3])
    -2
    """

    # Copy scores, but change +2 to +1 and -2 to -1 if confidence < 3. The m in
    # scores_m stands for modified.
    scores_m = list(map(
        lambda x, y: min(1, max(-1, x)) if abs(x) == 2 and y < 3 else x,
        scores, confis))
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
    correlation = (num_concordant_pairs - num_discordant_pairs) / \
            (math.sqrt(num_index_pairs_without_ties_1 *
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
                num_pairs_1 += p
                num_pairs_2 += p
    # Return the average penalty.
    return num_discordant_pairs / math.sqrt(num_pairs_1 * num_pairs_2)

if __name__ == "__main__":
    ee = EsaExperimentData()
    ee.read_all_score_files()
    ee.print_all_kendall_tau()

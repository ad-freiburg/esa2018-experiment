"""
Copyright 2019, University of Freiburg,
Chair of Algorithms and Data Structures.
Author: Hannah Bast <bast@cs.uni-freiburg.de>
"""

import itertools


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

        print("Kendall tau between rankings of the two PCs")
        tau1 = kendall_tau(self.avg_scores[0][0], self.avg_scores[0][1])
        tau2 = kendall_tau(self.avg_scores[1][0], self.avg_scores[1][1])
        tau3 = kendall_tau(self.avg_scores[2][0], self.avg_scores[2][1])
        print("Phase 1: %.2f" % tau1)
        print("Phase 2: %.2f" % tau2)
        print("Phase 3: %.2f" % tau3)

        print()
        print("Kendall tau between phases for same PC:")
        tau_pc1_12 = kendall_tau(self.avg_scores[0][0], self.avg_scores[1][0])
        tau_pc1_23 = kendall_tau(self.avg_scores[1][0], self.avg_scores[2][0])
        tau_pc2_12 = kendall_tau(self.avg_scores[0][1], self.avg_scores[1][1])
        tau_pc2_23 = kendall_tau(self.avg_scores[1][1], self.avg_scores[2][1])
        print("PC1, Phases 1 <-> 2: %.2f" % tau_pc1_12)
        print("PC2, Phases 1 <-> 2: %.2f" % tau_pc2_12)
        print("PC1, Phases 2 <-> 3: %.2f" % tau_pc1_23)
        print("PC2, Phases 2 <-> 3: %.2f" % tau_pc2_23)

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


def kendall_tau_ranks(scores):
    """
    Given a list of n scores, return a list of ranks. This is needed in
    function kendall_tau below.

    If all n scores are distinct, return i for the score that comes i-th in
    the sorted order of scores. If a score occurs multiple times, all
    occurrences of that score get the same rank and that rank is the average
    of the ranks these scores would receive if they were minimally perturbed
    so as to be distinct. See the doctest for an example.

    >>> kendall_tau_ranks([4, 2, 3, 1])
    [4.0, 2.0, 3.0, 1.0]
    >>> kendall_tau_ranks([3, 2, 2, 1])
    [4.0, 2.5, 2.5, 1.0]
    """

    # Compute buckets of the same score.
    buckets = {}
    for i, s in enumerate(scores):
        if s not in buckets:
            buckets[s] = []
        buckets[s].append(i)
    # Iterate over buckets and distribute ranks.
    last_rank = 0
    ranks = list(range(0, len(scores)))
    for s in sorted(buckets.keys()):
        n = len(buckets[s])
        # Average ties
        rank = last_rank + ((n + 1) / float(2))
        for i in buckets[s]:
            ranks[i] = rank
        last_rank += n
    return ranks


def kendall_tau(scores1, scores2, p=0.5):
    """
    Compute the p-normalized Kendall Tau as described in Fagin et al.:
    Comparing and Aggregating Rankings with Ties, PODS 2004
    https://dl.acm.org/citation.cfm?id=1055568

    For each pair i, j with i < j compare the order of the ranks of scores1[i]
    and scores1[j] with the order of the ranks of scores2[i] and scores2[j]. If
    the order is the same, there is no penalty. If the order is opposite, there
    is a penalty of one. If the ranks are the same for exactly one of the score
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

    >>> kendall_tau([1, 2, 3], [4, 5, 6])
    0.0
    >>> kendall_tau([1, 2, 3], [6, 5, 4])
    1.0
    >>> kendall_tau([4, 2, 3, 1], [3, 2, 2, 1]) # doctest:+ELLIPSIS
    0.08333...
    >>> kendall_tau([3, 2, 2, 1], [4, 2, 3, 1]) # doctest:+ELLIPSIS
    0.08333...
    """

    if len(scores1) == 1:
        return 0.0
    # First compute the ranks of the scores for each list.
    ranks1 = kendall_tau_ranks(scores1)
    ranks2 = kendall_tau_ranks(scores2)
    # Enumerate all possible pairs i, j with i < j.
    pairs = itertools.combinations(range(0, len(scores1)), 2)
    penalty = 0.0
    # Count the number of pairs in the second list (the ground truth), where
    # pairs with equal scores count only p (default 0.5, see above).
    num_ordered = 0.0
    for i, j in pairs:
        # The ranks of scores i and j in both score lists.
        a_i = ranks1[i]
        a_j = ranks1[j]
        b_i = ranks2[i]
        b_j = ranks2[j]
        # CASE 1: Scores i and j are different in both lists. Then there is a
        # penalty of 1.0 iff the order does not match.
        if a_i != a_j and b_i != b_j:
            if (a_i < a_j and b_i < b_j) or (a_i > a_j and b_i > b_j):
                pass
            else:
                penalty += 1
        # CASE 2: Scores i and j are the same in both lists. Then there is no
        # penalty.
        elif a_i == a_j and b_i == b_j:
            pass
        # CASE 3: Scores i and j are the same in one list, but different in the
        # other. Then there is a penalty of p (default value 0.5, see above).
        else:
            penalty += p
        # All pairs have a weight of 1. In the original paper, the weight is p
        # if the scores in list 2 (assumed to be the ground truth) as equal.
        if b_i != b_j:
            num_ordered += 1
        else:
            num_ordered += 1 # Original definition: += p
    # Return the average penalty.
    return penalty / num_ordered



if __name__ == "__main__":
    ee = EsaExperimentData()
    ee.read_all_score_files()
    ee.print_all_kendall_tau()

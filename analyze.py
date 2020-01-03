"""
Copyright 2019, University of Freiburg,
Chair of Algorithms and Data Structures.
Author: Hannah Bast <bast@cs.uni-freiburg.de>
"""

import sys
import math
import random
import pathlib

# Dictionary with long names for the score types above.
score_type_names = {
    "av": "confidence-weighted average score, from [-2..+2]",
    "l5": "rule-based score from {+2, +1, 0, -1, -2}",
    "l3u": "score from {+2, +1, -1} via l5, where -2, -1, 0 -> -1",
    "l3m": "score from {+1, 0, -1} via l5, where -2 -> -1 and +2 -> +1",
    "l3l": "score from {+1, -1, -2} via l5, where +2, +1, 0 -> +1",
    "l2u": "score from {+2, 0} via l5, where -2, -1, 0, +1 -> 0",
    "l2m": "score from {+1, -1} via l5, where +2, +1 -> +1",
    "l2l": "score from {0, -2} via l5, where -1, 0, +1, +2 -> 0",
    "av5": "av score, rounded to nearest score from {-2, -1, 0, +1, +2}",
    "av3u": "av5 score reduced to {+1, 0, -1} like l5 is reduced to l3u",
    "av3m": "av5 score reduced to {+1, 0, -1} like l5 is reduced to l3m",
    "av3l": "av5 score reduced to {+1, 0, -1} like l5 is reduced to l3l",
    "av2u": "av5 score, reduced to {+1, -1} like l5 is reduced to l2u",
    "av2m": "av5 score, reduced to {+1, -1} like l5 is reduced to l2m",
    "av2l": "av5 score, reduced to {+1, -1} like l5 is reduced to l2l",
    "avr": "fixed score from [-2..+2] with added Gaussian noise",
    "l5r": "random score from {+2,+1,0,-1,-2}, based on avr",
    "l3r": "random score from {+1,0,-1}, based on l5r, mapping from l3m",
    "l2r": "random score from {+1,-1}, based on l5r, mapping from l2m",
    "rnd": "completely random score from [-2..+2]"
}

# The score labels for the discrete ones of these. This is need to print the
# confusion matrices. The + in the +0 is important (or change code).
score_labels_by_type = {
    "l5": ["+2", "+1", "+0", "-1", "-2"],
    "l3u": ["+2", "+1", "-1"],
    "l3m": ["+1", "+0", "-1"],
    "l3l": ["+1", "-1", "-2"],
    "l2u": ["+2", "+0"],
    "l2m": ["+1", "-1"],
    "l2l": ["+0", "-2"],
    "av5": ["+2", "+1", "+0", "-1", "-2"],
    "av3u": ["+2", "+1", "-1"],
    "av3m": ["+1", "+0", "-1"],
    "av3l": ["+1", "-1", "-2"],
    "av2u": ["+2", "+0"],
    "av2m": ["+1", "-1"],
    "av2l": ["+0", "-2"],
    "avr": ["+2", "+1", "+0", "-1", "-2"],
    "l5r": ["+2", "+1", "+0", "-1", "-2"],
    "l3r": ["+1", "+0", "-1"],
    "l2r": ["+1", "-1"]
}

# Usage info printed when calling script without arguments.
usage_info = """
Usage: python3 analyze.py <score type> ...

Analyze the similarity of the rankings produced by the two PCs, where
<score type> specifies which score is used for each submission and PC:

av :   """ + score_type_names["av"] + """
l5 :   """ + score_type_names["l5"] + """
l3u:   """ + score_type_names["l3u"] + """
l3m:   """ + score_type_names["l3m"] + """
l3l:   """ + score_type_names["l3l"] + """
l2u:   """ + score_type_names["l2u"] + """
l2m:   """ + score_type_names["l2m"] + """
l2l:   """ + score_type_names["l2l"] + """
av5:   """ + score_type_names["av5"] + """
av3u:   """ + score_type_names["av3u"] + """
av3m:   """ + score_type_names["av3m"] + """
av3l:   """ + score_type_names["av3l"] + """
av2u:   """ + score_type_names["av2u"] + """
av2m:   """ + score_type_names["av2m"] + """
av2l:   """ + score_type_names["av2l"] + """
avr:   """ + score_type_names["avr"] + """
l5r:   """ + score_type_names["l5r"] + """
l3r:   """ + score_type_names["l3r"] + """
l2r:   """ + score_type_names["l2r"] + """
rnd:   """ + score_type_names["rnd"] + """

If multiple score types are specified, the analysis is dann for each score
type, one after the other.
"""


# Standard deviation of Gaussian noise for avr, l5r, l3r, l2r
#
# Note: a value of 0.8 gives the same Kendall tau as the real data
score_noise_standard_deviation = 0.8


class EsaExperimentData:

    def __init__(self):
        """
        The variable all_scores contains one list of score-confidence pairs for
        each PC and phase. Will be filled by read_all_score_files.
        """

        self.all_scores = [[[], []], [[], []], [[], []]]
        self.use_ansi_colors = True

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
        >>> test_input = [[(+1, 3), (+2, 3)], [(+2, 3)], [(-2, 3), (-1, 3)]]
        >>> ee.compute_scores(test_input, "l5")
        [1, 2, -2]
        >>> ee.compute_scores(test_input, "l3u")
        [1, 2, -1]
        >>> ee.compute_scores(test_input, "l3m")
        [1, 1, -1]
        >>> ee.compute_scores(test_input, "l3l")
        [1, 1, -2]
        >>> ee.compute_scores(test_input, "l2u")
        [0, 2, 0]
        >>> ee.compute_scores(test_input, "l2m")
        [1, 1, -1]
        >>> ee.compute_scores(test_input, "l2l")
        [0, 0, -2]
        >>> ee.compute_scores([[(+1, 3), (+2, 3), (+2, 3)]], "av5")
        [2]
        >>> ee.compute_scores([[(+1, 3), (+2, 3), (+2, 3)]], "av3m")
        [1]
        >>> ee.compute_scores([[(+1, 3), (+2, 3), (+2, 3)]], "av2m")
        [1]
        """

        sc_pairs = score_confidence_pairs
        l5_to_l3u_map = {+2: +2, +1: +1, +0: -1, -1: -1, -2: -1}
        l5_to_l3m_map = {+2: +1, +1: +1, +0: +0, -1: -1, -2: -1}
        l5_to_l3l_map = {+2: +1, +1: +1, +0: +1, -1: -1, -2: -2}
        l5_to_l2u_map = {+2: +2, +1: +0, +0: +0, -1: +0, -2: +0}
        l5_to_l2m_map = {+2: +1, +1: +1, +0: -1, -1: -1, -2: -1}
        l5_to_l2l_map = {+2: +0, +1: +0, +0: +0, -1: +0, -2: -2}
        if score_type == "av":
            return list(map(self.average_score, sc_pairs))
        elif score_type == "l5":
            return list(map(self.l5_score, sc_pairs))
        elif score_type == "l3u":
            return list(map(lambda x: l5_to_l3u_map[x],
                            self.compute_scores(sc_pairs, "l5")))
        elif score_type == "l3m":
            return list(map(lambda x: l5_to_l3m_map[x],
                            self.compute_scores(sc_pairs, "l5")))
        elif score_type == "l3l":
            return list(map(lambda x: l5_to_l3l_map[x],
                            self.compute_scores(sc_pairs, "l5")))
        elif score_type == "l2u":
            return list(map(lambda x: l5_to_l2u_map[x],
                            self.compute_scores(sc_pairs, "l5")))
        elif score_type == "l2m":
            return list(map(lambda x: l5_to_l2m_map[x],
                            self.compute_scores(sc_pairs, "l5")))
        elif score_type == "l2l":
            return list(map(lambda x: l5_to_l2l_map[x],
                            self.compute_scores(sc_pairs, "l5")))
        elif score_type == "av5":
            return list(map(lambda x: round(x),
                            self.compute_scores(sc_pairs, "av")))
        elif score_type == "av3u":
            return list(map(lambda x: l5_to_l3u_map[x],
                            self.compute_scores(sc_pairs, "av5")))
        elif score_type == "av3m":
            return list(map(lambda x: l5_to_l3m_map[x],
                            self.compute_scores(sc_pairs, "av5")))
        elif score_type == "av3l":
            return list(map(lambda x: l5_to_l3l_map[x],
                            self.compute_scores(sc_pairs, "av5")))
        elif score_type == "av2u":
            return list(map(lambda x: l5_to_l3u_map[x],
                            self.compute_scores(sc_pairs, "av5")))
        elif score_type == "av2m":
            return list(map(lambda x: l5_to_l3m_map[x],
                            self.compute_scores(sc_pairs, "av5")))
        elif score_type == "av2l":
            return list(map(lambda x: l5_to_l3l_map[x],
                            self.compute_scores(sc_pairs, "av5")))
        elif score_type == "avr":
            # Evenly spaced score from 2 to -2, with added Gaussian noise and
            # truncated to [-2..2] again.
            return [min(2, max(-2,
                    2 - 4 * score / (len(sc_pairs) - 1) +
                    random.gauss(0, score_noise_standard_deviation)))
                    for score in range(len(sc_pairs))]
        elif score_type == "l5r":
            return list(map(lambda x: round(x),
                            self.compute_scores(sc_pairs, "avr")))
        elif score_type == "l3r":
            return list(map(lambda x: l5_to_l3m_map[x],
                            self.compute_scores(sc_pairs, "l5r")))
        elif score_type == "l2r":
            return list(map(lambda x: l5_to_l2m_map[x],
                            self.compute_scores(sc_pairs, "l5r")))
        elif score_type == "rnd":
            return [random.random() * 4 - 2
                    for _ in range(len(sc_pairs))]

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

    def print_scores(self, scores, scores_file_base_name, subdir_name):
        """
        Print the scores to files <base_name>_phase<i>_pc<j>.txt in the given
        sub-directory. Create the sub-directory if it does not already exist.
        """

        print()
        print("Printing scores to sub-directory \"%s\"" % subdir_name)
        print()

        pathlib.Path(subdir_name).mkdir(exist_ok=True)
        base_name = scores_file_base_name
        file_names = []
        for i in range(3):
            for j in range(2):
                file_name = "tmp/%s-phase%d-pc%d.txt" % (base_name, i, j)
                file_names.append(file_name)
                with open(file_name, "w+") as file:
                    file.writelines("%.2f\n" % score for score in scores[i][j])

        gnuplot_script_name = "%s/plot-%s.p" % (subdir_name, score_type)
        print("Writing gnuplot script to show all scores, call like this:")
        print()
        print("\x1b[34mgnuplot -c %s\x1b[0m" % gnuplot_script_name)
        print()
        is_histogram = any(char.isdigit() for char in score_type)
        if not is_histogram:
            plot_arg = "\"< sort -n %s\""
            gnuplot_script = \
                "set key left top\n" + \
                "plot " + ", ".join(list(map(lambda x: plot_arg % x,
                                             file_names))) + "\n" + \
                "pause mouse"
        else:
            colors = ["#FFA07A", "#CD5C5C"]
            plot_arg = "\"%s\" " \
                       "using ($1%+.2f):(0,1) smooth freq with boxes " \
                       "linecolor rgb \"%s\""
            gnuplot_script = \
                "set key left top\n" + \
                "set boxwidth 0.1\n" + \
                "set style fill solid\n" + \
                "plot [] [:50] " + ", ".join(
                    list(map(lambda i, x: plot_arg %
                             (x, i/10 - 0.30 + 0.05 * (i//2), colors[i % 2]),
                             *zip(*list(enumerate(file_names)))))) + "\n" + \
                "pause mouse"

        print("Here is the script (for your curiosity)")
        print()
        print(gnuplot_script)
        print()
        with open(gnuplot_script_name, "w+") as gnuplot_script_file:
            print(gnuplot_script, file=gnuplot_script_file)

    def print_kendall_tau(self, scores, score_type):
        """
        Print statistics for the given score type. See the usage_info string at
        the beginning of this file for the options. See function compute_scores
        for the details of how the scores are computed for each type.
        """

        print()
        print("Normalized Kendall tau distance (a / b / p)"
              "between PCs and phases:")
        print()
        tau_a_1 = kendall_tau_a(scores[0][0], scores[0][1])
        tau_a_2 = kendall_tau_a(scores[1][0], scores[1][1])
        tau_a_3 = kendall_tau_a(scores[2][0], scores[2][1])
        tau_b_1 = kendall_tau_b(scores[0][0], scores[0][1])
        tau_b_2 = kendall_tau_b(scores[1][0], scores[1][1])
        tau_b_3 = kendall_tau_b(scores[2][0], scores[2][1])
        tau_p_1 = kendall_tau_p(scores[0][0], scores[0][1])
        tau_p_2 = kendall_tau_p(scores[1][0], scores[1][1])
        tau_p_3 = kendall_tau_p(scores[2][0], scores[2][1])
        print("Phase 1: %.2f / %.2f / %.2f" % (tau_a_1, tau_b_1, tau_p_1))
        print("Phase 2: %.2f / %.2f / %.2f" % (tau_a_2, tau_b_2, tau_p_2))
        print("Phase 3: %.2f / %.2f / %.2f" % (tau_a_3, tau_b_3, tau_p_3))
        print()
        tau_a_pc1_12 = kendall_tau_a(scores[0][0], scores[1][0])
        tau_a_pc1_23 = kendall_tau_a(scores[1][0], scores[2][0])
        tau_a_pc2_12 = kendall_tau_a(scores[0][1], scores[1][1])
        tau_a_pc2_23 = kendall_tau_a(scores[1][1], scores[2][1])
        tau_b_pc1_12 = kendall_tau_b(scores[0][0], scores[1][0])
        tau_b_pc1_23 = kendall_tau_b(scores[1][0], scores[2][0])
        tau_b_pc2_12 = kendall_tau_b(scores[0][1], scores[1][1])
        tau_b_pc2_23 = kendall_tau_b(scores[1][1], scores[2][1])
        tau_p_pc1_12 = kendall_tau_p(scores[0][0], scores[1][0])
        tau_p_pc1_23 = kendall_tau_p(scores[1][0], scores[2][0])
        tau_p_pc2_12 = kendall_tau_p(scores[0][1], scores[1][1])
        tau_p_pc2_23 = kendall_tau_p(scores[1][1], scores[2][1])
        print("Phases 1 <-> 2, PC1: %.2f / %.2f / %.2f"
              % (tau_a_pc1_12, tau_b_pc1_12, tau_p_pc1_12))
        print("Phases 1 <-> 2, PC2: %.2f / %.2f / %.2f"
              % (tau_a_pc2_12, tau_b_pc2_12, tau_p_pc2_12))
        print()
        print("Phases 2 <-> 3, PC1: %.2f / %.2f / %.2f"
              % (tau_a_pc1_23, tau_b_pc1_23, tau_p_pc1_23))
        print("Phases 2 <-> 3, PC2: %.2f / %.2f / %.2f"
              % (tau_a_pc2_23, tau_b_pc2_23, tau_p_pc2_23))

    def print_confusion_matrices(self, scores, score_type, mode):
        """
        Print confusion matrices between PCs (mode == "pcs") or between phases
        (mode == "phases") side by side.
        """

        if score_type in score_labels_by_type:
            score_labels = score_labels_by_type[score_type]
        else:
            print()
            print("! Confusion matrices only work for discrete scores or score"
                  "type missing from score_labels_by_type in code")
            print()
            return

        if mode == "pcs":
            print()
            print("Confusion matrices between the two PCs for phases 1, 2, 3:")
            print()
            score_list_pairs = [(scores[0][0], scores[0][1]),
                                (scores[1][0], scores[1][1]),
                                (scores[2][0], scores[2][1])]
            self.print_confusion_matrices_helper(score_list_pairs,
                                                 score_labels)
        elif mode == "phases":
            print()
            print("Confusion matrices between phases "
                  "(PC1 1/2, PC1 2/3, PC2 1/2, PC2 2/3):")
            print()
            score_list_pairs = [(scores[0][0], scores[1][0]),
                                (scores[1][0], scores[2][0]),
                                (scores[0][1], scores[1][1]),
                                (scores[1][1], scores[2][1])]
            self.print_confusion_matrices_helper(score_list_pairs,
                                                 score_labels)

    def print_confusion_matrices_helper(self, score_list_pairs, score_labels):
        """
        Compute the confusion matrices for the given pairs of scores and print
        them side by side from left to right. Each score must be contained in
        score_labels, if formatted with %+2d

        >>> ee = EsaExperimentData()
        >>> ee.use_ansi_colors = False
        >>> score_list_pairs = [([+1, +1, +0, +0, -1, -1],
        ...                      [-1, -1, +0, +1, -1, -1])]
        >>> score_labels = ["+1", "+0", "-1"]
        >>> ee.print_confusion_matrices_helper(
        ...     score_list_pairs,
        ...     score_labels) # doctest: +NORMALIZE_WHITESPACE
             +1 +0 -1
        +1    0  0  2
        +0    1  1  0
        -1    0  0  2
        """

        # Compute values of confusion matrices
        confusion_matrices = []
        for score_list_pair in score_list_pairs:
            confusion_matrix = {}
            for x in score_labels:
                confusion_matrix[x] = {}
                for y in score_labels:
                    confusion_matrix[x][y] = 0
            assert len(score_list_pair[0]) == len(score_list_pair[1])
            n = len(score_list_pair[0])
            for i in range(n):
                x = "%+d" % score_list_pair[0][i]
                y = "%+d" % score_list_pair[1][i]
                confusion_matrix[x][y] += 1
            confusion_matrices.append(confusion_matrix)

        # Print confusion matrices side by side
        k = len(confusion_matrices)
        format_string = "%2s   " + ("%2s " * len(score_labels) + "   ") * k
        color_codes_by_distance = [30, 34, 36, 31, 31]  # bold, blue, cyan, red
        print(format_string % tuple([""] + score_labels * k))
        print()
        for x in score_labels:
            entries = ["%2s" % x]
            for confusion_matrix in confusion_matrices:
                for y in score_labels:
                    color = color_codes_by_distance[abs(int(x) - int(y))]
                    if self.use_ansi_colors:
                        entries.append("\x1b[%dm%2s\x1b[0m" %
                                       (color, confusion_matrix[x][y]))
                    else:
                        entries.append("%2s" % confusion_matrix[x][y])
            print(format_string % tuple(entries))


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

    When there are ties, we have nc = N - nd - nt, where nt is the number of
    pairs, which are neither concordant or discordant (that is, one or both
    relations are ==). Then the correlation becomes 1 - 2 * (nd + nt/2) / N and
    the distance is (nd + nt/2) / N. That is, it's like counting each tied pair
    like half a concordant pair. This is very similar to variant p of the
    Kendall tau below with p = 0.5, except that there pairs which are tied on
    both sides are counted as 0, and the denumerator decreases a bit for every
    tied pair.

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
    if len(sys.argv) < 2 or sys.argv[1].endswith("help"):
        print(usage_info)
        sys.exit(1)

    modes = []
    while sys.argv[-1].startswith("--"):
        modes.append(sys.argv.pop())
    modes.reverse()
    if len(modes) == 0:
        modes = ["--kendall"]

    ee = EsaExperimentData()
    ee.read_all_score_files()

    for score_type in sys.argv[1:]:
        if score_type not in score_type_names:
            print()
            print("Score type \"%s\" does not exist or is not yet implemented"
                  % score_type)
            print(usage_info)
            sys.exit(1)

        scores = [[[], []], [[], []], [[], []]]
        scores[0][0] = ee.compute_scores(ee.all_scores[0][0], score_type)
        scores[0][1] = ee.compute_scores(ee.all_scores[0][1], score_type)
        scores[1][0] = ee.compute_scores(ee.all_scores[1][0], score_type)
        scores[1][1] = ee.compute_scores(ee.all_scores[1][1], score_type)
        scores[2][0] = ee.compute_scores(ee.all_scores[2][0], score_type)
        scores[2][1] = ee.compute_scores(ee.all_scores[2][1], score_type)

        score_type_name = score_type_names[score_type]
        print()
        print("\x1b[1mScore type \"%s\": %s\x1b[0m" %
              (score_type, score_type_name))

        for mode in modes:
            if mode == "--kendall":
                ee.print_kendall_tau(scores, score_type)
            elif mode == "--print":
                ee.print_scores(scores, score_type, "tmp")  # in subdir "tmp"
            elif mode == "--confusion-pcs":
                ee.print_confusion_matrices(scores, score_type, "pcs")
            elif mode == "--confusion-phases":
                ee.print_confusion_matrices(scores, score_type, "phases")
            else:
                print()
                print("Invalid mode: \"%s\" ... skipping it" % mode)

        print()

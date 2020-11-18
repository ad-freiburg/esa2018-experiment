# Data, code, slides and blog post of the ESA 2018 Experiment

*If you have any questions about this repository, please feel free to open an issue or send me an email at bast@cs.uni-freiburg.de with subject "ESA 2018 experiment".*

The ESA 2018 Experiment was an in-depth analysis of two parallel program committees reviewing the complete set of submissions independently.
This repository provides the (anonymized) data behind the experiment, we well as a Python script to analyze and visualize the data in various ways.
It also contains a draft of a post soon to be published on the CACM Blog: https://github.com/ad-freiburg/esa2018-experiment/blob/master/BLOGPOST.md
The slides from the report presented at the business meeting of the conference
can be found here: http://ad-publications.informatik.uni-freiburg.de/ESA_experiment_Bast_2018.pdf

Here are explanation of a few details from the blog post, which also explain how the `analyze.py` script works.
Some of the explanations refer to the slides from the link above.

1. If a fraction p<sub>i</sub> of the papers are accepted with probability a<sub>i</sub>, then the expected overlap is Σ<sub>i</sub> p<sub>i</sub> a<sub>i</sub><sup>2</sup> / Σ<sub>i</sub> p<sub>i</sub> a<sub>i</sub>. For the simple model, where each paper is accepted independently from the others with the same fixed acceptance rate, the expected overlap is simply that acceptance rate.

2. See slide 5 for the exact semantics of the scores. See slide 9 for the detailed scores of the 9 papers, which were a "clear accept" in at least one PC.

3. Run `python3 analyze.py` to see the definition of the `l5` score for each paper (a single rule-based score from -2, -1, 0, +1, +2). It is also explained on slide 10. To see the confusion matrix between the two PCs after each phase, run `python3 analyze.py l5 --confusion-pcs`. To see how often which score was given by which PC, run `python3 analyze.py l5 --print` and execute the produced gnuplot script. The bars on the left show the clear rejects after each reviewing phase.

4. To compute the Kendall tau correlation of the upper part of the ranking of the two PCs, run `python3 analyze.py avt`. The script also explains the `avt` score (the l5 score, but set to zero if not at least one reviewer gave the paper a +2). To compute the p-values of an R-test, run `python3 analyze.py avt --rtest`.

# Format of the data files

## Format of the six files scores-phase<n>-pc<i>.tsv

There were three reviewing phases (for each PC separately, at no point did the
two PCs communicate with each other):

Phase 1: Each PC Member provided their reviews with scores, without seeing any
of the reviews from the other PC members.

Phase 2: For each submission, discussion amongst the PC members assigend to that
submission. PC members were asked to updated not only the review but also the
score in case they upadated their opinion about a submission.

Phase 3: Discussion of "gray-zone" submissions (for which no accept or reject
decision had been reached yet) among all PC members. Again, PC members were
asked to update not only the review but also the score. Final voting on the
still undecided papers.

There is one file for each phase and each PC. Each of these files has exactly 51
lines (the number of valid submissions). The files for phases one and two have
exactly eight columns, the files for the third phase have exactly nine columns. The
format of the first eight columns is, where TAB is a tabulator, score is a score
from the set {+2, +1, 0, -1, -2} and confidence is a number from the set {1, 2,
3, 4, 5}.

<score>TAB<conf>TAB<score>TAB<conf>TAB<score>TAB<conf>TAB<score>TAB<conf>

The first six columns are always non-empty because each submission received at
least three reviews. Columns seven and eight are mostly empty, except for a few
submissions which received four reviews. No submission received more than four
reviews.

The files for the third phase have an additional ninth column containing the
result of the vote. A vote for a submission by a PC member was simply another
score and confidence based on a short summary of the discussion on the paper
at that point. For each submission voted on, a so-called "PC score" was computed
as the confidence-weighted average of the votes for that submission. The final
score for the submission was then computed as the confidence-weighted average of
the review scores at that point and the PC score, where the confidence for the
PC score was taken as 5.

# The ESA 2018 Peer Reviewing Experiment

## PART 1 [Introduction + Setup of the Experiment]

The European Symposium on Algorithms (ESA) is a venerable algorithms conference.
For its 26th edition in 2018, we have decided to set up an experiment to evaluate the quality of the peer reviewing process via two parallel program committees (PCs).
Each PC reviewed the complete set of submissions completely independently from each other.
The experiment is similar in spirit to the well-known NIPS 2014 experiment, but with more detailed data and a deeper analysis.

The experiment was conducted for Track B of the conference, dedicated to algorithms engineering, applications and empirical evaluation.
There were 51 valid submissions and two PCs with 12 members each.
The composition of the two PCs were the same with respect to gender, seniority, continent and research area.
For each PC, each submission was assigned to at least three PC members, and each PC member had 12-13 papers to review.
Overall 313 reviews were written, where about one third came from subreviewers picked by the PC members.
Each PC followed the same standard reviewing "algorithm", which was agreed on and laid out in advance as clearly as possible.
Each PC had the goal to select 10-12 papers for acceptance, which corresponds to an acceptance rate of 20 - 25%.
From the authors' perspective, a paper was accepted in the end if at least one of the two PCs selected it for acceptance.

As usual, reviewing proceeded in three phases:
In Phase 1, PC members entered their reviews without seeing any of the other reviews.
In Phase 2, PC members discussed with each other, mostly on a per-paper basis, and papers were proposed for acceptance / rejection in rounds.
In Phase 3, the remaining ("grey zone") papers were compared with each other and all papers left without a clear decision in the end were decided by voting.
PC members were explicitly and repeatedly asked to also update the *score* of their review whenever they changed something in their review.
This allowed a quantitative analysis of the various phases of the reviewing process.
For more details on the setup (and on the results), see http://ad-publications.informatik.uni-freiburg.de/ESA_experiment_Bast_2018.pdf

## PART 2 [Main Results]

**What is the overlap in the set of accepted papers?**
This was the number reported by the NIPS experiment, where the overlap was 43%.
It is an easy number to understand, but not the best number to look at, since it depends heavily on exactly how many papers are accepted.
In the ESA experiment, the overlap was 67% after Phase 1, 75% after Phase 2, and 58% after Phase 3 when considering an acceptance rate of 23.5% for each PC
(for the NIPS experiment, the acceptance rate was 22.5%).

To put these figures into perspective, let us look at a few simple random models.
If the reviewing algorithm were deterministic, the overlap would be 100%.
If a random subset of papers was accepted by each PC, the expected overlap would be 24%.
In a more realistic model, 10% of the papers are accepted with probability 0.8, 20% of the papers are accepted with probability 0.6, 20% of the papers are accepted with probability 0.1, and 50% of the papers have no chance to be accepted.
Then the expected overlap is around 60%.

**How many clear accepts were there?**
The score range for each review was +2, +1, 0, -1, -2 (clear accept, weak accept, borderline, weak reject, clear reject).
For a paper that received only +2 scores, there was no incentive for discussion and these papers were accepted right away.
There was little agreement between the two PCs concerning such "clear accepts".
Out of 9 papers that were clear accepts in one PC, 4 were rejected by the other PC and only 2 were also clear accepts in the other PC.
So telling our experiment, there is little evidence that something like a "clear accept" exists. If it exists, there are very few.

**How effective were the various reviewing phases?**
The overlap in the number of accepted papers showed a strange behavior:
It increased after Phase 2 (per-paper discussions), but after Phase 3 (discussion of grey-zone papers and voting) it was worse than after Phase 1 (independent reviews without any interaction between the reviewers whatsoever).
We investigated this in more detail by looking at the normalized Kendall tau distance between the **upper part** of the rankings of the two PCs after each phase.
The normalized Kendall tau distance is the percentage of all pairs of submissions that were ordered oppositely in the two PCs,
with a tie in one PC and a non-tie in the other PC counting as 0.5.
Before we report the result, let us understand how we ranked the papers and why we only looked at the upper part of that ranking.

Papers were ranked by their confidence-weighted average score and this score was set to zero if no reviewer advocated the paper by giving a +2.
This makes sense for the following two reasons:
First, PC members were informed before that a paper needs at least one +2 to be accepted
and that the goal of the discussion phase is that the score set for a paper properly reflects the collective opinion of the assigned reviewers on that paper.
Second, there is no incentive for the reviewers to rank the papers that will be rejected;
by setting their score to zero, they will effectively not be considered for the Kendall tau distance.

The normalized Kendall tau distance was 27% after the first phase, 18% after the second phase, and 21% after the third phase.
In Phase 2, around 20% of all 313 reviews were modified relevant to the upper part of the ranking
That is, a previous score of +1 or +2 was changed or a lower score was changed to +1 or +2.
The bottom line is that the second phase (per-paper discussions) was reasonably effective,
while the final phase (discussion of grey zone papers and voting) was not effective or even counter-productive.
TODO: say which % difference is statistically significant here.

**How many clear rejects were there?**
After Phase 3, there were 20 clear rejects in PC1 and 17 clear rejects in PC2
and none of these papers were considered for acceptance in the other PC (in the sense that one reviewer advocated for them by giving a +2).
These number were also improved by the discussion phase, while the last phase changed nothing.
Around 40% of the submissions were thus clear rejects in the sense that it is unlikely that any other PC (of similar quality) would have accepted any of them.

There was only one paper with a score difference of 3 or more between the two PCs.
It was a clear accept in one PC (all reviewers gave it a +2) and thus wasn't discussed any further after the first phase.
The other PC was very critical of the meaningfulness of the results, so that the paper was eventually rejected with an overall score of -1.

**In summary:**
The PCs did a very good job in separating the wheat from the chaff.
There also appeared to be at least a partial order in the wheat, which the discussions helped to identify better.
The discussion of the gray zone produced random results and could just as well have been omitted.

It is important to note that the above results should be considered **a lower bound**
for the consistency of a reviewing process at a computer science conference, for the following reasons.
First, ESA is a medium-sized conference (around 300 submissions to both tracks) with a relatively tightly-knit community.
Second, for the sake of comparability the moderation of the two PCs was conducted with particularly great care:
Most PCs nowadays do their work mostly or fully electronically without meeting personally.
This is especially problematic for the discussion phase, since it can be hard to distinguish
whether a PC member has nothing to add to his or her previous argument or whether they simply forgot or did not bother to reply because of other obligations.
For this experiment, great care was taken that no discussion threads stalled and to remind PC members to give feedback.
Also, the reviewing "algorithm" was laid out beforehand in great detail.
Fourth, the PCs were selected with particular care and comparable diversity.
Neglecting any of these factors adds further randomness to the process,
and so the results from this experiment are really what is left when you control for these other factors as much as possible.

## PART 3 [Consequences]

I see four main conclusions from this experiment:

**First, we need more experiments of this kind.**
For computer science, we have the NIPS experiment and now the ESA experiment.
They give a first picture, but given the central importance of peer review for our profession, we need more data points.
As a side effect, this will also help to raise awareness further.
One argument I often hear is that it is too much effort, in particular, with respect to the additional number of reviewers needed.
I don't buy this argument.
There are so many conferences in computer science, many of them very large.
If we pick one of these conferences from time to time to make an experiment, the additional load is negligible in the big picture.
Another argument I often hear is that it is an unsolvable problem.
This always leaves me speechless.
In their respective specialty, researchers love hard problems and sometimes work their whole life trying to make some progress.
But when it comes to peer reviewing, there is nothing we can do?

**Second, we need to truly accept the results of these experiments.**
The experiments so far provide strong hints that there is a significant signal in reviews, but also a significant amount of noise and randomness.
Yet, many PCs seem blissfully unaware that their reviewing process happens in a bubble.
Just image one PC heatedly debating the merits of a paper in the alleged gray zone,
which in another PC (that judges the same set of papers) does not receive much attention because it was accepted or rejected early on.
There are at least two strong and well-known biases at work here.
One is that many people are unaware of their biases and thus **feel** that they are way more objective than they actually are.
Another is if you make a strong effort as a group, than the result has to be meaningful.
To this day, I often hear PC chairs say that there was a clear boundary between the papers that got accepted and those that had to be rejected.
Such statements are simply not supported by any evidence.
The other extreme are fatalists who feel that the whole process is random anyway, so why bother to provide a proper review.
Both of these extremes are wrong, and this is still not widely understood or acted upon.

**Third, how do we incorporate these results to improve the reviewing process?**
Let us assume that the results from the NIPS and the ESA experiment are no anomalies, but will be replicated in future experiments.
Then there are some pretty straightforward ways how we can incorporate them into the current reviewing process.
For example, discussion of papers in the so-called "gray zone" (which is often very large) could be dropped, saving everybody precious time.
For the per-paper discussions, care should be taken that the scores are updated according to the discussion,
so that the overall score reflects the final state of the discussion.
These scores could then be converted to a probability distribution for at least a subset of the papers,
namely those which have a chance to be accepted (at least one reviewer advocated their acceptance), but do not have unanimously strong support.
Papers from this "extended gray zone" could then be accepted with a probability according to this distribution, that is, proportional to their score.
This would not make the process any more random, but definitely less biased.

Finally, if reviewing indeed manages to separate the wheat from the chaff, a simple and effective measurement to decrease randomness would be to accept more papers.
Low acceptance rates, especially for conferences, come from a time where proceedings were printed and every paper was presented in a longer talk.
Much as changed in the meantime.
Digital publication no longer imposes a limit on the number of papers and many conferences have already moved away from the "one full talk per paper" principle.
TODO: write a bit more here and end on a high note.

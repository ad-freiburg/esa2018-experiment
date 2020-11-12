# Quo Vadis Peer Review: The ESA 2018 Experiment

## From the "NIPS Experiment" to the "ESA experiment"

In 2014, the organizers of the Conference on Neural Information Processing Systems (NeurIPS, then still called NIPS) made a bold experiment.
They split their program committee in two and let each half **independently** review a part of the submissions.
The interesting part was that they made the parts **overlap**, so that 10% of all submissions (166 papers) were reviewed by two independent PCs.
The result of this experiment was essentially a single figure: the overlap in the number of accepted papers.
The overlap was only 43%, that is, more than half of the papers accepted by one PC were rejected by the other.
This led to a passionate flare-up of the old debate of how effective or random peer-reviewing really is.

The experiment left open a number of interesting questions:

1. How many papers that looked like "clear accepts" in one PC were rejected by the other PC?
2. How many papers that looked like "clear rejects" in one PC were accepted by the other PC?
3. How large is the "gray zone" of papers, which are neither fish nor foul and how well do the PCs agree on these?
4. How do these similarities evolve over the reviewing process: Do the per-paper discussions really help? Do the often extensive discussions of papers in the gray zone help?
5. And finally, what does this all mean for the future of peer review?

To answer these questions, in 2018 we set up an experiment similar to the NIPS experiment, but with richer data and a deeper analysis.
The target was the 26th edition of the "European Symposium on Algorithms" (ESA), a venerable algorithms conference.
ESA receives around 300 submissions every year and has two tracks: the more theoretical Track A and the more practical Track B.
For the experiment, we picked Track B, which received 51 submissions that year.
Two independent PCs of 12 members each were set up, with the same distribution with respect to gender, seniority, continent and research area.
Overall 313 reviews were written.
These numbers are smaller than for the NIPS experiment, but still large enough to yield meaningful results, yet small enough to allow for the time-intensive deeper analysis.

Each PC had the goal to select 10-12 papers for acceptance, which corresponds to an acceptance rate of 20 - 25% (in the NIPS experiment, the acceptance rate was 22.5%).
Both PCs followed the same standard reviewing "algorithm", which was agreed on and laid out in advance as clearly as possible:

Phase 1: PC members entered their reviews without seeing any of the other reviews.
Phase 2: PC members discussed with each other, mostly on a per-paper basis, and papers were proposed for acceptance / rejection in rounds.
Phase 3: The remaining ("gray zone") papers were compared with each other and all papers left without a clear decision in the end were decided by voting.

PC members were explicitly and repeatedly asked to also update the *score*  of their review whenever they changed something in their review.
This allowed a quantitative analysis of the various phases of the reviewing process.
For more details on the setup (and on the results), see http://ad-publications.informatik.uni-freiburg.de/ESA_experiment_Bast_2018.pdf

## PART 2: The main results of the ESA experiment

Let us first get an overview of the results and then, in Part 3, discuss their implications.

**What is the overlap in the set of accepted papers?**
In the NIPS experiment, the overlap was 43%.
In the ESA experiment, the overlap was 67% after Phase 1, 75% after Phase 2, and 58% after Phase 3 (see below concerning the up and down).
For both experiments, the acceptance rate per PC was 23%.
To put these figures into perspective:
If the reviewing algorithm was deterministic, the overlap would be 100%.
If a random subset of papers was accepted by each PC, the expected overlap would be 24%.
In a more realistic model, where 10% / 20% / 20% / 50% of the papers are accepted with probabilities 0.8 / 0.6 / 0.1 / 0.0, the expected overlap is around 60%.

**How many clear accepts were there?**
The score range for each review was +2, +1, 0, -1, -2.
The use of 0 was discouraged and it was communicated beforehand that only papers with a +2 from at least one reviewer were considered for acceptance.
For a paper that received only +2 scores, there was no incentive for discussion and these papers were accepted right away.
There was little agreement between the two PCs concerning such "clear accepts".
Out of 9 papers that were clear accepts in one PC, 4 were rejected by the other PC and only 2 were also clear accepts in the other PC.
If papers that are "clear accepts" exist at all, they are very few.

**How many clear rejects were there?**
After Phase 2, there were 20 clear rejects in PC1 and 17 clear rejects in PC2
None of these papers were even considered for acceptance in the other PC.
Those number are larger than after Phase 1 (before the discussions), but did not change anymore after Phase 3 (gray-zone discussions).
At least one third of the submissions were thus clear rejects in the sense that it is unlikely that any other PC would have accepted any of them.
There was only one paper with a score difference of 3 or more between the two PCs.
It was a clear accept in one PC (all reviewers gave it a +2, praising the strong results), while the other PC was very critical of its meaningfulness.

**How effective were the various reviewing phases?**
The overlap in the number of accepted papers fluctuated between 58% and 75% over the reviewing process, but these changes were not statistically significant.
We investigated this in more detail by comparing the *rankings* of the two PCs of those papers that were at least considered for acceptance (at least one reviewer speaks up) from phase to phase.
Ranking similarity was computed using the normalized Kendall tau distance (1 if the rankings are identical, 0 if one ranking is the reverse of the other); see [1] for the details.
The similarity was 36% after Phase 1, 27% after Phase 2, and 30% after Phase 3, where the drop after Phase 1 is statistically significant.
This surprising result questions the efficiency of the discussion phases.
Is the *independence* of the initial reviews a valuable feature?

**In summary, the PCs did a very good job in separating the wheat from the chaff.
There also appeared to be at least a partial order in the wheat.
But it is completely unclear whether the extensive discussions helped or even harmed.**

It is important to note that the above results should be considered **a lower bound**
for the consistency of a reviewing process at a computer science conference, for the following reasons.
First, ESA is a medium-sized conference with a relatively tightly-knit community and one-tier PCs.
Second, for the sake of comparability the moderation of the two PCs in this experiment was conducted with particularly great care:
Most PCs nowadays do their work mostly or fully electronically without meeting personally.
This is especially problematic for the discussion phase, where discussions frequently stall
and it is unclear whether that is because the PC members have nothing to add to their previous argument
or whether they simply forgot or did not bother to reply because of other obligations.
For this experiment, great care was taken that no discussion threads stalled and to remind PC members to give feedback.
Third, the reviewing "algorithm" was laid out beforehand in great detail.
Fourth, the PCs were selected with particular care and diversity (with respect to seniority, gender, topic, continent) as similar as possible.
Neglecting any of these factors adds further randomness to the process.
The results from this experiment are therefore really what is left when you control for these other factors as much as possible.

## PART 3: What now?

I see four main conclusions from this experiment:

**First, we need more experiments of this kind.**
We have the NIPS experiment and now the ESA experiment.
FOOTNOTE: There are other experiments, like the single-blind vs. double-blind comparison at WSDM'17, investigating particular aspects of the reviewing process.
They give a first impression, but important questions are still not clear enough (for example, how effective or even harmful the discussions are).
One argument I often hear is that it is too much effort, in particular, with respect to the additional number of reviewers needed.
I don't buy this argument.
There are so many conferences in computer science, many of them very large.
If we pick one of these conferences from time to time to make an experiment, the additional load is negligible in the big picture.
Another argument I often hear is that it is an unsolvable problem.
This always leaves me speechless.
In their respective specialty, researchers love hard problems and sometimes work their whole life trying to make some progress.
But when it comes to peer reviewing, the current status quo is as good as it gets?

**Second, we need to truly accept the results of these experiments.**
The experiments so far provide strong hints that there is a significant signal in reviews, but also a significant amount of noise and randomness.
Yet, many PCs spend a lot of time debating papers, blissfully unaware that another PC in a parallel universe did not give these papers much attentions because they were accepted or more likely rejected early on in the process.
From my own extensive PC experience, I conjecture that there are at least two strong biases at work here.
One is that humans tend to be unaware of their biases and feel that they are much more objective than they actually are.
Another is the feeling that if you make a strong effort as a group, than the result has to be meaningful and not random.
To this day, I often hear PC chairs (who worked very hard) say that there was a clear boundary between the papers that got accepted and those that were rejected.
It is usually acknowledged that there is a gray zone, but not that that "gray zone" might encompass almost all of the papers which are not clear rejects.
The other extreme is fatalism: the feeling that the whole process is random anyway, so why bother to provide a proper review.
Both of these extremes are wrong, and this is still not widely understood or acted upon.

**Third, how do we incorporate these results to improve the reviewing process?**
Let us assume that the results from the NIPS and the ESA experiment are no anomalies.
Then the discussion phase could be shortened, saving everybody time and decreasing turn-around times.
This, however, must be countered by measures to ensure that the initial reviews are of reasonable quality (I conjecture that the embarrassment of writing a sub-standard review is an important factor in reviewing).
When ranking submissions by average weighted scores, it is crucial to communicate the semantics of these scores very clearly and in advance.
Average scores could then be converted to a probability distribution for at least for a subset of the papers,
namely those which have a chance to be accepted (at least one reviewer speaks up), but which do not have unanimously strong support.
Papers from this "extended gray zone" could then be accepted with a probability proportional to their score.
This would not make the process any more random, but definitely less biased.
To reduce not only bias, but also randomness, a simple and effective measure would be to accept more papers.
Low acceptance rates for conferences come from a time where proceedings were printed and every paper was presented in a longer talk.
Much has changed in the meantime.
Digital publication no longer imposes a limit on the number of papers and many conferences have already moved away from the "one full talk per paper" principle.

**Fourth, all of this knowledge has to be preserved from one PC to the next.**
Already now, we have a treasure of knowledge on the peer reviewing process.
But only a fraction of it is considered or implemented at any particular conference.
The main reason is the typical way in which administrative jobs are implemented in the academic world.
Jobs rotate (often rather quickly), there is little incentive to excel, there is almost no quality control,
and participating in the peer-reviewing process is another obligation on top of an already more than full-time job.
You do get status points for some administrative jobs, but you do not really get points for doing them particularly well or for investing an outstanding amount of time or energy.
Why is that so?
Most scientists are inherently self-motivated and incredibly perseverant when it comes to their science.
Indeed, that is why most of us became scientists in the first place.
Administrative tasks are not what we signed up for, not what we were trained for and not what we were selected for.
We understand intellectually how important they are, but we do not really treat them that way.

**The bottom line:
Peer review is a very hard and complex problem, but there is still a lot of room for improvement with respect to the current status quo.
Three key ingredients are: more experiments and more data (treating peer review like a research problem), better knowledge transfer from one PC to the next (implementing what we already know is good), an effective incentive system (promote and reward excellence in this essential part of science).** 

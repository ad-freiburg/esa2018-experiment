# How Objective is Peer Review: The ESA 2018 Experiment

## PART 1: From the "NIPS Experiment" to the "ESA Experiment"

In 2014, the organizers of the Conference on Neural Information Processing Systems (NeurIPS, then still called NIPS) made a bold experiment.
They split their program committee (PC) in two and let each half **independently** review a bit more than half of the submissions.
That way 10% of all submissions (166 papers) were reviewed by two independent PCs.
The result of the experiment was that among these 166 papers, the set of accepted papers from the two PCs overlapped by only 43%.
That is, more than half of the papers accepted by one PC were rejected by the other.
This led to a passionate flare-up of the old debate of how effective or random peer-reviewing really is.

The experiment left open a number of interesting questions:

1. How many papers that looked like "clear" accepts in one PC were rejected by the other PC, if any?
2. How many papers that looked like "clear" rejects in one PC were accepted by the other PC, if any?
3. How well do the rankings of the two PCs correlate and is there a natural cutoff for the number of accepted papers?
4. Do the discussions of the papers between PC members help decrease the randomness of the decisions?
5. And finally, what does this all mean for the future of peer review?

To answer these questions, in 2018 I conducted an experiment similar to the NIPS experiment, but with richer data and a deeper analysis.
The target was the 26th edition of the "European Symposium on Algorithms" (ESA), a venerable algorithms conference.
ESA receives around 300 submissions every year and has two tracks: the more theoretical Track A and the more practical Track B.
For the experiment, I picked Track B, which received 51 submissions that year.
Two independent PCs of 12 members each were set up, who produced a total of 313 reviews, each of which was later analyzed in detail. 
These numbers are smaller than for the NIPS experiment, but still large enough to yield meaningful results, yet small enough to allow for the time-intensive deeper analysis.

Each PC had the goal to select 10-12 papers for acceptance, which corresponds to an acceptance rate of 20 - 25% (in the NIPS experiment, the acceptance rate was 22.5%).
Both PCs followed the same standard reviewing "algorithm", which was agreed on and laid out in advance as clearly as possible:

- Phase 1: PC members entered their reviews without seeing any of the other reviews.
- Phase 2: PC members discussed with each other, mostly on a per-paper basis, and papers were proposed for acceptance / rejection in rounds.
- Phase 3: The remaining ("gray zone") papers were compared with each other and all papers left without a clear decision in the end were decided by voting.

PC members were explicitly and repeatedly asked to also update the *score*  of their review whenever they changed something in their review.
This allowed a quantitative analysis of the various phases of the reviewing process.
For more details on the setup and on the results and the (anonymized) data, see the website of the experiment.<sup>1</sup>

## PART 2: The main results of the ESA experiment

Let us first get a quick overview of the results and then, in Part 3, discuss their implications.

**What is the overlap in the set of accepted papers?**
In the NIPS experiment, the overlap was 43%.
In the ESA experiment, the overlap was 58%.
For both experiments, the acceptance rate per PC was 23%.
To put these figures into perspective:
If the reviewing algorithm was deterministic, the overlap would be 100%.
If a random subset of papers was accepted by each PC, the expected overlap would be 24%.
If 10% / 20% / 20% / 50% of the papers were accepted with probabilities 0.8 / 0.6 / 0.1 / 0.0, the expected overlap would be around 60%.
The overlap is not the best number to look at, since it depends rather heavily on the number of accepted papers; read on.

**How many clear accepts were there?**
The score range for each review was +2, +1, 0, -1, -2.
The use of 0 was discouraged and it was communicated beforehand that only papers with a +2 from at least one reviewer were considered for acceptance.
For a paper that received only +2 scores, there was no incentive for discussion and these papers were accepted right away.
There was little agreement between the two PCs concerning such "clear accepts".
Out of 9 papers that were clear accepts in one PC, 4 were rejected by the other PC and only 2 were also clear accepts in the other PC (that is, 4% of all submissions).
If papers that are "clear accepts" exist at all, they are very few.

**How many clear rejects were there?**
There were 20 clear rejects in PC1 and 17 clear rejects in PC2.
None of these papers were even considered for acceptance in the other PC.
At least one third of the submissions were thus clear rejects in the sense that it is unlikely that any other PC would have accepted any of them.
There was only a single paper with a score difference of 3 or more between the two PCs.
It was a clear accept in one PC (all reviewers gave it a +2, praising the strong results), while the other PC was very critical of its meaningfulness.

**Is there a natural cutoff to determine the set of accepted papers?**
For a rate of accepted papers of 10%, the overlap in the set of accepted papers was 40% (corresponding to the 4% "clear accepts").
For rates between 14% to 40%, the overlap varied rather erratically between 54% and 70%.
Increasing the rate of accepted papers beyond that, showed a steady increase in the overlap (due to the "clear rejects" at the bottom).
There is no natural cutoff short of the "clear rejects".

**How effective were the various reviewing phases?**
We have seen that the overlap for a fixed acceptance rate is a rather unreliable measure.
I therefore also compared the *rankings* of the two PCs among those papers for which at least one reviewer considered acceptance.
Ranking similarity was computed via the Kendall tau correleation (1 for identical rankings, 0 for random rankings, -1 if one is the reverse of the other); see the website for details.<sup>1</sup>
This similarity was 46% after Phase 1, 66% after Phase 2, and 62% after Phase 3, where the increase after Phase 1 is statistically significant (p = 0.02).
This suggests that the per-paper discussions play an important role for objectifying paper scores,
while any further discussions add little or nothing in that respect.
This correlates well with the experience that PC members are willing to adapt their scores *once* after reading the reviews from the other PC members,
but after that, their opinion is more or less fixed.

**In summary, the PCs did a good job in separating the wheat from the chaff.
There appeared to be at least a partial order in the wheat, but there is no natural cutoff.
The fewer papers are accepted, the more random is the selection.
The initial per-paper discussions helped to make the review scores more objective.
Any further discussions had no measurable effect.**

It is important to note that the above results should be considered **a lower bound**
for the consistency of the reviewing process at a computer science conference, for the following reasons:

1. ESA is a medium-sized conference with a relatively tightly-knit community and a one-tier PC.
2. In online discussions, threads frequently stall because PC members forget or not bother to reply because of other obligations.
For this experiment, great care was taken to remind PC members to give feedback so that no discussion threads stalled.
3. The reviewing "algorithm" was laid out beforehand in detail.
4. The PCs were selected so that their diversity (with respect to seniority, gender, topic, continent) was as similar as possible.

Larger conference, two-tier PCs, unresponsive PC members, underspecified guidelines, and variance in diversity
most likely all further increase the randomness in the reviewing process.

## PART 3: What now?

I see four main conclusions from this experiment:

**First, we need more experiments of this kind.**
We have the NIPS experiment and now the ESA experiment.<sup>2</sup>
They give a first impression, but important questions are still open.
For example, it would be very valuable to redo the experiment above for a larger and more heterogeneous conference.
One argument I often hear is that it is too much effort, in particular, with respect to the additional number of reviewers needed.
I don't buy this argument.
There are so many conferences in computer science, many of them very large.
If we pick one of these conferences from time to time to make an experiment, the additional load is negligible in the big picture.
Another argument I often hear is that it is an unsolvable problem.
This always leaves me speechless.
In their respective specialty, researchers love hard problems and sometimes work their whole life trying to make some progress.
But when it comes to the reviewing process, the current status quo is as good as it gets?

**Second, we need to truly accept the results of these experiments.**
The experiments so far provide strong hints that there is a significant signal in reviews, but also a significant amount of noise and randomness.
Yet, to this day, the myth of a natural cutoff for determining the set of accepted papers prevails.
It is usually acknowledged that there is a gray zone, but not that that "gray zone" might encompass almost all of the papers which are not clear rejects.
PCs can spend a lot of time debating papers, blissfully unaware that another PC in a parallel universe did not give these papers much attention because they were accepted or more likely rejected early on in the process.
From my own PC experience, I conjecture that there are at least two biases at work here.
One is that humans tend to be unaware of their biases and feel that they are much more objective than they actually are.
Another is the feeling that if you make a strong effort as a group, then the result is meaningful and fair.
The other extreme is fatalism: the feeling that the whole process is random anyway, so why bother to provide a proper review.
Both of these extremes are wrong, and this is still not widely understood or acted upon.

**Third, how do we incorporate these results to improve the reviewing process?**
Let us assume that the results from the NIPS and the ESA experiment are not anomalies.
Then there are some pretty straightforward ways how we can incorporate them into the current reviewing process.
For example, discussion of papers in the alleged "gray zone" could be dropped.
Instead, this energy could be used to communicate and implement the semantics of the available scores as clearly as possible in advance.
Average scores could then be converted to a probability distribution for at least a subset of the papers,
namely those for which at least one but not all reviewers spoke up.
Papers from this "extended gray zone" could then be accepted with a probability proportional to their score.
This would not make the process any more random, but definitely less biased.
To reduce not only bias, but also randomness, a simple and effective measure would be to accept more papers.
Digital publication no longer imposes a limit on the number of accepted papers
and many conferences have already moved away from the "one full talk per paper" principle.

**Fourth, all of this knowledge has to be preserved from one PC to the next.**
Already now, we have a treasure of knowledge on the peer reviewing process.
But only a fraction of it is considered or implemented at any particular conference.
The main reason I see is the typical way in which administrative jobs are implemented in the academic world.
Jobs rotate (often rather quickly), there is little incentive to excel, there is almost no quality control (who reviews the reviewers),
and participation in the peer-reviewing process is another obligation on top of an already more than full-time job.
You do get status points for some administrative jobs, but not for doing them particularly well or for investing an outstanding amount of time or energy.
Most of us are inherently self-motivated and incredibly perseverant when it comes to our science.
Indeed, that is why most of us became scientists in the first place.
Administrative tasks are not what we signed up for, not what we were trained for and not what we were selected for.
We understand intellectually how important they are, but we do not really treat them that way.

**My bottom line:
The reputation of the peer-review process is tarnished.
Let us work on this with the same love and attention we give to our favorite research problems.
Let us do more experiments to gain insights that help us make the process more fair and regain some trust.
And let us create powerful incentives, so that whatever we already know is good is actually implemented
and carried over from one PC to the next.**

<sup>1</sup> https://github.com/ad-freiburg/esa2018-experiment

<sup>2</sup> There are other experiments, like the single-blind vs. double-blind comparison at WSDM'17, investigating particular aspects of the reviewing process.


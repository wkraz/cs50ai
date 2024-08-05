"""
NOTES
Uncertainty
-----------
omega - represents a "world" that occurs when some action happens
P(w) - how to represent the probability of that world
    always between 0 and 1, inclusive
    summing P(w) of all worlds has to equal 1

unconditional probability - degree of belief in a proposition in the absence of any other evidence
conditional probability - opposite of ^
P(a | b) - representing conditional probability
    represents conditional probability
    a: what we want probability of
    b: evidence
    "what is the probability of a given b"
P(a | b) = P(a \land b) / P(b)

if a and b are independent: P(a \land b) = P(a)P(b | a)
    rolling dice ex: P(a = 6 and b = 6) = P(a = 6)P(b = 6) = 1/36

Bayes Rule:
P(b | a) = P(b)P(a | b) / P(a)
    P(a) is just a constant, so you can also represent this as: P(b | a) = c * P(b)P(a | b)

joint probability distribution - table that shows probability of two things happening at once
P(a, b)

Some probability rules:
P(negation a) = 1 - P(a)
P(a \lor b) = P(a) + P(b) - P(a \land b)
    remove double counting (inclusion/exclusion set theory)
P(a) = P(a, b) + P(a, negation b) - marginalization
    only 2 cases: either b happens or b doesn't happen, and they're independent
P(a) = P(a|b)P(b) + P(a|not b)P(not b) - conditioning

bayesian network - data structure that represents dependencies among random variables
    directed graph (individual nodes w/ arrows that connect each other)
    each node represents a random variable
    arrow from X to Y means X is a parent of Y
    each node has probability distribution p(X | Parents(X))
        think of parents as causes for some event to occur

inference - given query X and evidence e, we want to calculate P(X | e)
    if e doesn't contain all the variables, then you will have hidden variables
        iterate over all possible values of the hidden variables and add up their probabilities
P(X | e) = alpha * P(X, e) = alpha * \sum_y P(x, e, y) # where y loops over the range of all possible values of hidden variables

sampling - sampling a random choice from every node and multiply them together to get the probability distribution
    powerful because you can look at how many samples a condition is true in to get a good estimate

likelihood weighting
    first, fix the values for evidence variables so we don't sample them too
    sample the non-evidence variables using conditional probabilities in Bayesian network
    weight each sample by its likelihood - the probability of all the evidence

Markov Models
    sometimes we want to get probabilities of things that change over time and are not discrete
    represent P(X_t) as the probability of event X at time t
    Markov assumption - the assumption that the current state depends only on a finite, fixed number of previous states
        when looking at the weather, we only have to look at the past couple days, not the past year
    example assumption: I can predict tomorrow's weather based off today's
    Markov chain is a chain of assumptions that rely on each other
        X_0 -> X_1 -> X_2 ...
        "when it's sunny it tends to stay sunny"

hidden markov model
    Markov model w/ hidden states that generate an event
    there can be multiple "layers" of Markov models that can connect to each other
        ex: the weather depends on itself, so does if people bring umbrellas, but umbrellas also rely on the weather

"""
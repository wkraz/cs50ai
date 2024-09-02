# Analysis

## Layer 2, Head 2

Hi, do you [MASK] anything from the store?

Thoughts:
- This attention layer is very focused on neighboring words. Given the linear flow of this sentence, it makes plenty of sense
and it makes a nice diagonal of white squares
- In this case, [MASK] is a verb (have, need, want - per the program), and the closest relationship to 255 is between [MASK] and a direct
object: 'anything'

## Layer 5, Head 6

Hi, do you [MASK] anything from the store?

Thoughts:
- This attention layer is focused on prepositions and their relationships with noun phrases. Here, the most obvious relationship
is between 'from' and 'store'
- There is a lot of other noise in this attention layer, specifically with the head's [SEP], which we can just ignore

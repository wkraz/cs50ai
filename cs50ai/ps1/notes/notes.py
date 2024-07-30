"""
NOTES
Knowledge
-------------
we can encode logic to the computer through propositional logic (hooray discrete!)
model - assignment of a truth value to every propositional symbol
knowledge base - a set of sentences known by a knowledge-based agent
a ⊨ b : entailment 
    in every model in which sentence a is true, sentence b is also true
    ex: a = "I know that it is a Tuesday in January"
        b = "I know that it is January"
        if a is true then b is automatically true because a "entails" it

inference - process of deriving new sentences from old ones
model checking - we want to determine if our knowledge base entails a query: alpha (KB ⊨ alpha)
    enumerate all possible models
    check every model where kb is true and see if alpha is true
        if not, then kb does not entail alpha

can think of theorem proving like a search problem:
    initial state - starting knowledge base
    actions - inference rules
    transition model - new knowledge base after inference
    goal test - check statement we're trying to prove
    path cost function - number of steps in proof

resolution - way of inference
want to determine if kb ⊨ a 
do this by checking if kb and neg(a) is a contradiction (just proof by contradiction)
    if so, then kb ⊨ a
    assume kb \land a and move stuff around until you find a contradiction (literally just discrete)



"""

import sys 

class Node(): # just in case :)
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action      

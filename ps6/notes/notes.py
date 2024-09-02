"""
Language
----------

NP -> D N 
    - noun phrase: ex: the (D) city (N)
VP -> V NP
    - verb then noun phrase
S -> NP VP 
    - noun phrase verb phrase

nltk
    library that makes parsing sentences easier
    
n-gram
    contiguous sequence of n items from a sample of text
    built in function in nltk
    
markov chains
    markovify - library 

naive bayes classifier
    useful for looking at which statements have a positive/negative connotation
    ex: P(positive | "my grandson loved it") => pretty high
    ends up being __proportional__ to P(positive, "my", "grandson", "loved", "it")
        not equal to normal bayes rule
    THEN we say this is naively proportional to:
        P(positive)P("my"|positive)P("grandson"|positive)P("loved"|positive)P("it"|positive)
    Then we simply calculate P(positive) = # positive samples / # total samples

word representation - we want to translate words into numbers so we can do things like neural networks
ex: "he wrote a book"
    he - [1, 0, 0, 0]
    wrote - [0, 1, 0, 0]
    a - [0, 0, 1, 0]
    book - [0, 0, 0, 1]
this is one-hot representation -- not ideal b/c it can get ginormous and don't relate to each other in meaningful ways
instead, we want a distributed representation
    we will define a word based on the words that appear around it
word2vec is something we can use to align words that are close to each other
    gives words vector representations
    we can look at the distance between two words (0 is closest, 1 is farthest)
    
attention - most important words in a sentence
    what is the capital of the United States?
    highest attention scores - capital, united states (just represented by nums 0-1)
        we want our neural network to learn the most important words and figure out what is happening
        
transformers 
    each word goes through the neural network, independent of the other ones
    however, this makes it so that we lose the ordering of the words
        to fix this, we add a vector of positional encoding to the input word
        resulting vector captures input word and where it occurs in the sentence
    after this, we want to run multiple self-attention layers on the input so we can figure out how important it is and learn from it
    

"""
import markovify
import nltk

n_grams = nltk.ngrams

text = [] # mock data
# training markov model with markovify library 
text_model = markovify.Text(text)

# classifying an input sample using naive bayes classifying in nltk library 
classifier = nltk.NaiveBayesClassifier.train(text)


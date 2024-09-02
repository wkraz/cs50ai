import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
S -> VP
S -> S Conj S 
S -> NP VP PP

NP -> N
NP -> Det N
NP -> Adj NP
NP -> Det Adj N
NP -> N PP

VP -> V
VP -> V NP
VP -> V Adv
VP -> V PP
VP -> V NP PP
VP -> VP Conj VP

PP -> P NP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    
    words = nltk.word_tokenize(sentence) # tokenize
    
    new_words = []
    for word in words:
        lower_word = word.lower()
        found = False
        for letter in lower_word:
            if letter.isalpha():
                found = True
                break
                
        if found:
            new_words.append(lower_word)
            
    return new_words
                
    
def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    chunks = []
    
    for subtree in tree.subtrees():
        if subtree.label() == 'NP' and not any(child.label() == 'NP' for child in subtree.subtrees() if child != subtree):
            chunks.append(subtree)
    
    return chunks


if __name__ == "__main__":
    main()

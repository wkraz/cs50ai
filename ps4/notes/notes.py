"""
Machine Learning
NOTES
-----------------

supervised learning - given a data set of input-output pairs, learn a function that maps inputs to outputs
classification - task of learning a function mapping an input point to a discrete category
    supervised means that a human goes in and labels certain data input points

k-nearest neighbor classification 
    algorithm that chooses the most common class out of the k nearest data points to the input

perceptron classification
    creating a "best fit line" that makes a line that separates two classes from each other
    alternative approach to k-nearest neighbors
    mathematically -
        let x1 = humidity, x2 = pressure
        h(x1, x2) = 1 (rain) if w0 + w1x1 + w2x2 >= 0 (w represents weights)
                  = 0 (no rain) otherwise
        represent w0, w1, w2 as a vector: w (w0, w1, w2)
        represent input vector as x: (1, x1, x2)
        you're just taking dot product: w * x
    perceptron learning rule: 
        given data point (x, y), update each weight given by:
            wi = wi + a(y  - h(x)) cross xi
            start out with random weights and keep updating by this formula
            x = estimate, y = actual output
            
regression
    task of learning a function mapping an input point to a continuous value
    
loss function - function that expresses how poorly a hypothesis performs
    looking at difference between actual and estimated outputs
    ex: 0-1 loss function
        L(actual, predicted) = 0 if actual == predicted, 1 otherwise
    L1 loss function: returns |actual - predicted|
    L2: (actual - predicted) ^ 2 # more harshly punishes values that are crazy off
    
regularization - penalizing hypotheses that are more complex and favoring more general solutions

holdout cross-validation - splitting data into a training set and a test set
k fold cross-validation - the same thing but using k - 1 training sets and 1 test set

scikit-learn - most popular ML library
    implementation
        assign a ML algorithm to model (Perceptron for example) # important to try multiple and see what does the best
        create training and testing datasets
        model.fit(x_training, y_training) # to train model
        predictions = model.predict(x_testing) # to make predictions on testing set
        now compare predictions to y_testing by using loss function of your choice
            correct = (y_testing == predictions).sum()
            incorrect = (y_testing != predictions).sum()
            total = len(predictions)
            accuracy = correct / total
            
reinforcement learning
    given a set of rewards or punishments, learn what actions to take in the future
    agent is given a state inside of an environment, they make an action, and receive a new state as a result
        they are then given a reward based on this action
        has to learn what actions it should take in the future based off these
    Markov Decision Process is a model that we use to represent state, action, and reward
        set of states S; set of actions ACTIONS(s); transition model P(s'|s, a)
            given a state and actual, what's the probability i enter a new state: s'
        reward function R(s, a, s')
        
Q-learning
    method of learning a function Q(s, a), which estimates the reward value of performing an action in a state
    implementation
        start with Q(s, a) = 0 for all s, a (you haven't done anything so no experience to lean on)
        when we take an action and receive a reward: estimate the value of Q(s, a) based on current reward and expected future rewards
            balancing act of current rewards and future rewards:
        update Q(s, a) to take into account old estimate AND our new estimate
    greedy decision-making - when in state s, choose a with highest Q(s, a)
    epsilon-greedy - with probability epsilon, choose random move, else choose best move (so you explore best solution)
    
Nim 
    pyramid-like pile of objects, players take turns removing objects, whoever is left with 1 loses
        look at how many rows there are, number of objects in each row, and how many you want to remove each turn
    from nim import train, play # functions implemented in nim.py
    ai = train(10,000) # play against itself 10,000 times and train off that
    play(ai)

function approximation
    instead of learning Q(s, a) for every state-action pair, learn how to estimate it

unsupervised learning
    learning patterns from input data without any additional feedback
    clustering is a way to implement this
        cluster data points that are similar together
        k-means clustering 
            divides all data points into k different clusters 
            repeatedly assigns points to clusters and updates those clusters' centers




"""
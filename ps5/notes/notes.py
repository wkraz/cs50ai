"""
Neural Networks
---------------

logistic sigmoid - type of activation function
    function that "draws the line" and makes a classification based on data - rainy vs. not rainy
    g(x) = e^x / (e^x + 1)

neural network structure
    2 nodes (x1, x2) point to an output node
    edges are represented as weights (w1, w2)
    output node: g(w0 + w1x1 + w2x2)
    can add more than 2 nodes, function is just sum of xiwi + w0
    
gradient descent - algorithm for minimizing loss when training neural network
    gradient = direction the loss function is moving in
    want to look at direction loss is moving in, and move weights the other way
    approach:
        start with random choice of weights
        repeat:
            calculate gradient based on all (want to optimize) data points: direction we should move the weights towards
            update weights according to the gradient (small step)
            
multilayer neural network
    input layer, output layer, and 1+ hidden layer in between input & output

backpropogation
    algorithm for training neural networks with hidden layers
    start at output and backtrack 
    approach:
        start with random choice of weights
        repeat:
            calculate error for output layer 
            for each layer, starting with output layer and moving inwards towards earliest hidden layer:
                propogate error back one layer 
                update weights
                
deep neural network - neural network w/ multiple hidden layers 

overfitting - being overreliant on input data and not making general enough conclusions
dropout - overfitting technique
    temporarily removing units (randomly) to prevent over-reliance on certain units

computer vision
    take every single pixel and add it to the input layer 
    
image convolution
    applying a filter that adds each pixel value to its neighbors, weighted according to kernel matrix
    used to get observations by looking at a pixel and its neighbors
    useful for edge detection - returns high value if edge, near-zero value if not edge
    
pooling
    reducing the size of an input by sampling from regions in the input
    max-pooling - pooling by choosing the max value in each region
    
convolutional neural network (CNN)
    start w/ grid of pixels and apply a convolution (filtering) step multiple times
    run a pooling step on these convolutions to reduce their dimensions
    optional --- you can do more convolutions/pooling on the result to keep reducing size of input
    when done, flatten these all into a single array and feed it into an input layer of a neural network
    now, the input is much smaller and has most of the useful features and you learn features of the input in the process
        edges, curves, shapes, objects, etc
    
feed-forward neural network - only has connections one way -- left to right
    input -> network (computations) -> output
    
recurrent neural network
    generates output that gets fed back into itself for future inputs
    instead of input -> network -> output:
        input -> network -> output
                    |
                network -> output
                    |
                network -> output...
        each network gets input from the past network's output
        

"""


# using tensorflow
import tensorflow as tf
import sys

"""
simple neural network 
"""

X_training, y_training, X_testing, y_testing = None # mock training sets

# create neural network
model = tf.keras.models.Sequential() # sequential model from keras API

# add a hidden layer with 8 units, with ReLU activation (type of activation function)
model.add(tf.keras.layers.Dense(8, input_shape=(4,), activation="relu"))

# add output layer with 1 unit, with sigmoid activation (type of activation function)
model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

# train neural network
model.compile(
    optimizer="adam", # model to optimize weights
    loss="binary_crossentropy", # model to record loss function
    metrics=["accuracy"] # what do we care about: accuracy
)
model.fit(X_training, y_training, epochs=20) # now actually train the model (go through 20 times (epochs))

"""
CNN example
"""

# evaluate how well model works
model.evaluate(X_testing, y_testing, verbose=2)

mnist = tf.keras.datasets.mnist # MNIST handwriting dataset is built into tensorflow

# prepare data for training
(x_train, y_train), (x_test, y_test) = mnist.load_data()
model2 = tf.keras.models.Sequential([
    
    # convulational layer, learn 32 filters with a 3x3 kernel
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(28, 28, 1)
    ),
    
    # max pooling layer with a 2x2 pool size
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)), 
    
    # flatten units
    tf.keras.layers.Flatten(),
    
    # add a hidden layer with 128 units and a dropout to prevent overreliance (drop half the points)
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.5),
    
    # add an output layer with output units for all 10 digits
    # softmax takes the output and turns it into a probibility distribution
    tf.keras.layers.Dense(10, activation="softmax")
])

# train neural network
model2.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
model2.fit(x_train, y_train, epochs=10)

# evaluate performance
model2.evaluate(x_test, y_test, verbose=2)

# save model to file (if we want)
if len(sys.argv) == 2:
    filename = sys.argv[1]
    model.save(filename)
    print(f'Model saved to {filename}.')
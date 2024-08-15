# Neural Network Project Thought Process

I decided to create a Sequential neural network using the keras API. 
I first started with a singular convolutional/pooling layer where I learned 32 filters with a 3x3 kernel, and used max pooling with a 2x2 pool size to reduce the size of the input.
I realized that my accuracy was still quite low, so I added two more convolutional/pooling layers where I doubled the filters learned each time and ran 2x2 max pooling each time.
I then flattened my data and added a hidden layer with 128 units and a dropout of 0.5.
I then added an output layer of size: NUM_CATEGORIES, for each type of sign. I then compiled the network with Keras algorithms, and reached an accuracy of 0.9785

### TLDR: accuracy: 0.9785 - loss: 0.0823
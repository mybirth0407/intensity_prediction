# Numeric Python Library.
import numpy as np
# Keras perceptron neuron layer implementation.
from keras.layers import Dense
# Keras Dropout layer implementation.
from keras.layers import Dropout
# Keras Activation Function layer implementation.
from keras.layers import Activation
# Keras Model object.
from keras.models import Sequential

# Peraring dataset
# Imports csv into pandas DataFrame object.
dataset = np.loadtxt('./train_test.txt', dtype='float64')
# split into input (X) and output (Y) variables
x_train = dataset[:, 0:-1]
y_train = dataset[:, -1]


test_dataset = np.loadtxt('./02CompRef_P5_VU_11_2_0.01.txt', dtype='float64')
x_test = test_dataset[:, 0:-1]
y_test = test_dataset[:, -1]

# create model
model = Sequential()

model.add(Dense(731, input_dim=731, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(182, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(45, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(11, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))

# Compile model
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(x_train, y_train, epochs=150, batch_size=100)

# evaluate the model
scores = model.evaluate(x_test, y_test)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))


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
# Get System Argument
import sys


def main(argv):
  data_train = np.loadtxt(argv[1], dtype='float32')
  x_train = data_train[:, 0:-1]
  y_train = data_train[:, -1]

  data_test = np.loadtxt(argv[2], dtype='float32')
  x_test = data_test[:, 0:-1]
  y_test = data_test[:, -1]

  # create model
  model = Sequential()
  
  model.add(Dense(731, input_dim=731, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(365, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(182, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(91, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(40, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(12, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(10, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(5, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(2, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(1, activation='sigmoid'))

  model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

  # Fit the model
  model.fit(x_train, y_train, epochs=50, batch_size=100)

  # evaluate the model
  scores = model.evaluate(x_test, y_test)
  print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

if __name__ == '__main__':
  main(sys.argv)
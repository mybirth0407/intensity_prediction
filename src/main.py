# Numeric Python Library.
import numpy as np
from keras import metrics
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
  epochs = int(argv[1])
  batch_size = int(argv[2])
  data_train = np.loadtxt(argv[3], dtype='float32')
  x_train = data_train[:, 0:722]
  y_train = data_train[:, -10:]

  data_test = np.loadtxt(argv[4], dtype='float32')
  x_test = data_test[:, 0:722]
  y_test = data_test[:, -10:]

  # create model
  model = Sequential()
  
  model.add(Dense(722, input_dim=722, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(650, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(600, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(550, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(500, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(450, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(400, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(350, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(300, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(250, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(200, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(150, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(100, activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(50, activation='relu'))
  model.add(Dense(10, activation='sigmoid'))

  model.compile(loss='mean_squared_error', optimizer='adam',
                metrics=[metrics.mean_squared_error])

  # Fit the model
  model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

  # evaluate the model
  scores = model.evaluate(x_test, y_test)
  predict = model.predict(x_test, batch_size=32)
  print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
  print(predict)

if __name__ == '__main__':
  main(sys.argv)